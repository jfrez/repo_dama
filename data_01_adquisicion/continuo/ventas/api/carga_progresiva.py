#!/usr/bin/env python
"""
Carga continua desde un API (o fixture) para órdenes, líneas, pagos e inventario.
Inserta sólo registros recientes según EDU_PROGRESSIVE_LOOKBACK_DAYS.
"""

from __future__ import annotations

import datetime as dt
import json
import os
from pathlib import Path
from typing import Dict, Tuple

import pandas as pd
import requests
from prefect import flow, task

from utils_edu.db import log_step, record_run, write_dataframe


FIXTURE = Path(__file__).resolve().parent / "fixtures" / "ventas_incremental.json"
API_MODE = os.getenv("EDU_API_MODE", "offline").lower()
API_URL = os.getenv("EDU_API_URL")
LOOKBACK_DAYS = int(os.getenv("EDU_PROGRESSIVE_LOOKBACK_DAYS", "7"))
# Nota: modo offline usa el fixture para que el flujo sea reproducible sin depender de red.


def _filter_recent(df: pd.DataFrame, column: str, lookback_days: int) -> pd.DataFrame:
    """Recorta un DataFrame a la ventana de lookback sobre la columna indicada."""
    # Paso utilitario: recorta la ventana de actualización
    if df.empty:
        return df
    cutoff = dt.datetime.utcnow() - dt.timedelta(days=lookback_days)
    df[column] = pd.to_datetime(df[column], errors="coerce")
    return df[df[column] >= cutoff]


@task
def load_from_source() -> Dict[str, pd.DataFrame]:
    """Obtiene datos desde API real o fixture y los devuelve como DataFrames."""
    # DAMA: Data Acquisition (fuente continua API/fixture)
    if API_MODE == "online" and API_URL:
        log_step("API", f"Consultando {API_URL}")
        resp = requests.get(API_URL, timeout=15)
        resp.raise_for_status()
        payload = resp.json()
    else:
        log_step("API", f"Usando fixture {FIXTURE.name}")
        payload = json.loads(FIXTURE.read_text())
    origin = "online" if (API_MODE == "online" and API_URL) else "fixture"

    orders = pd.DataFrame(payload.get("orders", []))
    items = pd.DataFrame(payload.get("order_items", []))
    payments = pd.DataFrame(payload.get("payments", []))
    inventory = pd.DataFrame(payload.get("inventory", []))
    for df in (orders, items, payments, inventory):
        df["source"] = origin
    return {"orders": orders, "items": items, "payments": payments, "inventory": inventory}


@task
def normalize(data: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
    """Normaliza tipos/columnas de órdenes, ítems, pagos e inventario."""
    # DAMA: Data Quality (tipado y selección de columnas críticas)
    log_step("API", "Normalizando estructuras")
    orders = data["orders"]
    items = data["items"]
    payments = data["payments"]
    inventory = data["inventory"]

    if not orders.empty:
        orders["total_amount"] = pd.to_numeric(orders["total_amount"], errors="coerce")
        orders["updated_at"] = pd.to_datetime(orders["updated_at"], errors="coerce")
        orders["order_date"] = pd.to_datetime(orders["order_date"], errors="coerce")
        orders = orders[
            ["order_id", "customer_id", "order_date", "status", "currency", "total_amount", "updated_at", "source"]
        ]

    if not items.empty:
        items["quantity"] = pd.to_numeric(items["quantity"], errors="coerce").fillna(0).astype(int)
        items["unit_price"] = pd.to_numeric(items["unit_price"], errors="coerce")
        items["updated_at"] = pd.to_datetime(items["updated_at"], errors="coerce")
        items = items[["order_id", "line_number", "sku", "quantity", "unit_price", "currency", "updated_at", "source"]]

    if not payments.empty:
        payments["amount"] = pd.to_numeric(payments["amount"], errors="coerce")
        payments["updated_at"] = pd.to_datetime(payments["updated_at"], errors="coerce")
        payments["paid_at"] = pd.to_datetime(payments.get("paid_at"), errors="coerce")
        payments = payments[
            ["payment_id", "order_id", "method", "status", "amount", "currency", "paid_at", "updated_at", "source"]
        ]

    if not inventory.empty:
        inventory["stock"] = pd.to_numeric(inventory["stock"], errors="coerce").fillna(0).astype(int)
        inventory["updated_at"] = pd.to_datetime(inventory["updated_at"], errors="coerce")
        inventory = inventory[["sku", "warehouse", "stock", "updated_at", "source"]]

    return {"orders": orders, "items": items, "payments": payments, "inventory": inventory}


@task
def apply_incremental(data: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
    """Aplica ventana incremental según LOOKBACK_DAYS para cada entidad."""
    # DAMA: Data Security/Operations (ventana incremental controlada)
    filtered = {
        key: _filter_recent(df, "updated_at", LOOKBACK_DAYS) for key, df in data.items() if isinstance(df, pd.DataFrame)
    }
    log_step("API", f"Ventana {LOOKBACK_DAYS} días: orders={len(filtered.get('orders', []))} registros")
    return filtered


@task
def persist(data: Dict[str, pd.DataFrame]) -> Tuple[int, int, int, int]:
    # DAMA: Data Storage & Traceability (escritura en raw + control)
    """Persiste entidades normalizadas en tablas raw y retorna conteos por tipo."""
    inserted_orders = inserted_items = inserted_payments = inserted_inventory = 0
    if not data.get("orders", pd.DataFrame()).empty:
        payload = data["orders"].copy()
        # Mantiene histórico incremental (append) formateando fechas a cadenas ISO.
        payload["order_date"] = payload["order_date"].dt.strftime("%Y-%m-%d")
        payload["updated_at"] = payload["updated_at"].dt.strftime("%Y-%m-%dT%H:%M:%SZ")
        write_dataframe(payload, "raw_ordenes_api")
        inserted_orders = len(payload)
    if not data.get("items", pd.DataFrame()).empty:
        payload = data["items"].copy()
        payload["updated_at"] = payload["updated_at"].dt.strftime("%Y-%m-%dT%H:%M:%SZ")
        write_dataframe(payload, "raw_order_items_api")
        inserted_items = len(payload)
    if not data.get("payments", pd.DataFrame()).empty:
        payload = data["payments"].copy()
        payload["updated_at"] = payload["updated_at"].dt.strftime("%Y-%m-%dT%H:%M:%SZ")
        payload["paid_at"] = payload["paid_at"].dt.strftime("%Y-%m-%dT%H:%M:%SZ")
        write_dataframe(payload, "raw_payments_api")
        inserted_payments = len(payload)
    if not data.get("inventory", pd.DataFrame()).empty:
        payload = data["inventory"].copy()
        payload["updated_at"] = payload["updated_at"].dt.strftime("%Y-%m-%dT%H:%M:%SZ")
        write_dataframe(payload, "raw_inventory_api")
        inserted_inventory = len(payload)
    return inserted_orders, inserted_items, inserted_payments, inserted_inventory


@flow(name="edu_api_progressive_flow")
def run() -> None:
    """Flujo incremental desde API/fixture hacia tablas raw con trazabilidad."""
    try:
        # 1) Extraer (API o fixture)
        raw = load_from_source.submit().result()
        # 2) Normalizar estructuras y tipos
        normalized = normalize.submit(raw).result()
        # 3) Aplicar ventana incremental
        recent = apply_incremental.submit(normalized).result()
        # 4) Persistir en raw y registrar ejecución
        ins_orders, ins_items, ins_payments, ins_inventory = persist.submit(recent).result()
        detail = (
            f"orders={ins_orders}, items={ins_items}, payments={ins_payments}, inventory={ins_inventory}, modo={API_MODE}"
        )
        record_run("api_ventas_progressive", "OK", ins_orders + ins_items + ins_payments + ins_inventory, detail)
        log_step("API", f"Cargados {detail}")
    except Exception as exc:  # noqa: BLE001
        record_run("api_ventas_progressive", "ERROR", 0, str(exc))
        log_step("API", f"Fallo: {exc}")
        raise


if __name__ == "__main__":
    run()
