#!/usr/bin/env python
"""
Carga histórica de órdenes (cabecera y líneas) desde CSV a tablas raw.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from prefect import flow, task

from utils_edu.db import log_step, record_run, write_dataframe


ORDERS_CSV = Path(__file__).resolve().parent / "samples" / "ordenes.csv"
ITEMS_CSV = Path(__file__).resolve().parent / "samples" / "ordenes_items.csv"


@task
def load_orders(path: Path) -> pd.DataFrame:
    """Carga el CSV de cabecera de órdenes históricas."""
    # DAMA: Data Acquisition (cabecera de órdenes históricas)
    log_step("HIST-ORDENES", f"Leyendo {path}")
    return pd.read_csv(path)


@task
def load_items(path: Path) -> pd.DataFrame:
    """Carga el CSV de líneas de órdenes históricas."""
    # DAMA: Data Acquisition (detalle de órdenes)
    log_step("HIST-ORDENES", f"Leyendo {path}")
    return pd.read_csv(path)


@task
def normalize_orders(df: pd.DataFrame) -> pd.DataFrame:
    """Formatea fechas y montos de cabecera, reteniendo columnas clave."""
    # DAMA: Data Quality (fechas, montos y claves obligatorias)
    log_step("HIST-ORDENES", "Normalizando cabecera")
    # Harmoniza fechas para evitar mezclas de timezones o formatos al consolidar.
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce").dt.strftime("%Y-%m-%d")
    df["total_amount"] = pd.to_numeric(df["total_amount"], errors="coerce")
    df["updated_at"] = pd.to_datetime(df["updated_at"], errors="coerce").dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    cols = ["order_id", "customer_id", "order_date", "status", "currency", "total_amount", "updated_at"]
    return df[cols]


@task
def normalize_items(df: pd.DataFrame) -> pd.DataFrame:
    """Tipifica cantidades/precios y asegura estructura de líneas de orden."""
    # DAMA: Data Quality (cantidades y precios válidos)
    log_step("HIST-ORDENES", "Normalizando líneas")
    # Controla numéricos y asegura enteros en quantity para que cuadre con métricas posteriores.
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce").fillna(0).astype(int)
    df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")
    df["updated_at"] = pd.to_datetime(df["updated_at"], errors="coerce").dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    cols = ["order_id", "line_number", "sku", "quantity", "unit_price", "currency", "updated_at"]
    return df[cols]


@task
def persist_orders(df: pd.DataFrame) -> int:
    """Guarda cabeceras en raw_ordenes_csv sustituyendo contenido previo."""
    # DAMA: Data Storage/Operations (capa raw de cabecera)
    write_dataframe(df, "raw_ordenes_csv", if_exists="replace")
    return len(df)


@task
def persist_items(df: pd.DataFrame) -> int:
    """Guarda líneas en raw_order_items_csv sustituyendo contenido previo."""
    # DAMA: Data Storage/Operations (capa raw de líneas)
    write_dataframe(df, "raw_order_items_csv", if_exists="replace")
    return len(df)


@flow(name="edu_ordenes_initial_flow")
def run(orders_csv: str = str(ORDERS_CSV), items_csv: str = str(ITEMS_CSV)) -> None:
    """Orquesta la carga histórica de órdenes (cabecera + líneas) desde CSV."""
    try:
        # 1) Leer cabeceras e ítems
        df_orders = load_orders.submit(Path(orders_csv)).result()
        df_items = load_items.submit(Path(items_csv)).result()
        # 2) Normalizar cabeceras e ítems
        norm_orders = normalize_orders.submit(df_orders).result()
        norm_items = normalize_items.submit(df_items).result()

        # 3) Persistir en raw (cabecera y líneas)
        ins_orders = persist_orders.submit(norm_orders).result()
        ins_items = persist_items.submit(norm_items).result()

        log_step("HIST-ORDENES", f"Cargadas {ins_orders} órdenes y {ins_items} líneas")
        record_run(
            "historico_ordenes",
            "OK",
            ins_orders + ins_items,
            f"Archivos {Path(orders_csv).name}, {Path(items_csv).name}",
        )
    except Exception as exc:  # noqa: BLE001
        log_step("HIST-ORDENES", f"Fallo: {exc}")
        record_run("historico_ordenes", "ERROR", 0, str(exc))
        raise


if __name__ == "__main__":
    run()
