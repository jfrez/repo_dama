#!/usr/bin/env python
"""
Procesamiento y control de calidad de datos intermedios (ecommerce).

Genera `educacional/tmp/dq_resumen.csv` con hallazgos sobre órdenes, pagos e inventario.
"""

from __future__ import annotations

from pathlib import Path
from typing import List

import pandas as pd
from prefect import flow, task

from utils_edu.db import log_step, read_dataframe, record_run


OUTPUT = Path(__file__).resolve().parents[3] / "tmp" / "dq_resumen.csv"


def _summarize_orders(df: pd.DataFrame, items_agg: pd.DataFrame | None = None) -> dict:
    # DAMA: Data Quality — chequeos de completitud y consistencia monto vs ítems
    """Construye métricas de calidad para stage_ordenes (completitud y montos)."""
    if df.empty:
        return {"dataset": "stage_ordenes", "registros": 0, "issues": "sin datos"}
    missing_customer = int(df["customer_id"].isna().sum())
    negative_total = int((df["total_amount"] < 0).sum())
    mismatch_items = 0
    orphan_items = 0
    if items_agg is not None and not items_agg.empty:
        merged = df[["order_id", "total_amount"]].merge(items_agg, on="order_id", how="left")
        merged["items_amount"] = merged["items_amount"].fillna(0)
        mismatch_items = int((merged["total_amount"].sub(merged["items_amount"]).abs() > 0.01).sum())
        orphan_items = int((~items_agg["order_id"].isin(df["order_id"])).sum())
    issues_flag = any([missing_customer, negative_total, mismatch_items, orphan_items])
    return {
        "dataset": "stage_ordenes",
        "registros": len(df),
        "missing_customer": missing_customer,
        "negative_total": negative_total,
        "items_mismatch": mismatch_items,
        "items_huerfanos": orphan_items,
        "detalle": "revisar" if issues_flag else "ok",
    }


def _summarize_items(df: pd.DataFrame, valid_orders: set[str] | None = None) -> dict:
    # DAMA: Data Quality — validación de cantidades, precios y referencial en líneas
    """Devuelve resumen de hallazgos para stage_order_items (negativos, referencial)."""
    if df.empty:
        return {"dataset": "stage_order_items", "registros": 0, "issues": "sin datos"}
    negative_qty = int((df["quantity"] < 0).sum())
    negative_price = int((df["unit_price"] < 0).sum())
    orphan_lines = 0
    if valid_orders is not None:
        orphan_lines = int((~df["order_id"].isin(valid_orders)).sum())
    issues_flag = any([negative_qty, negative_price, orphan_lines])
    return {
        "dataset": "stage_order_items",
        "registros": len(df),
        "negative_qty": negative_qty,
        "negative_price": negative_price,
        "items_sin_orden": orphan_lines,
        "detalle": "revisar" if issues_flag else "ok",
    }


def _summarize_payments(df: pd.DataFrame) -> dict:
    # DAMA: Data Quality — coherencia de montos cobrados/pagados
    """Resume calidad de pagos: montos negativos y registros disponibles."""
    if df.empty:
        return {"dataset": "stage_payments", "registros": 0, "issues": "sin datos"}
    negative_amount = int((df["amount"] < 0).sum()) if "amount" in df else 0
    return {
        "dataset": "stage_payments",
        "registros": len(df),
        "negative_amount": negative_amount,
        "detalle": "revisar" if negative_amount else "ok",
    }


def _summarize_inventory(df: pd.DataFrame) -> dict:
    # DAMA: Data Quality — stock no negativo por SKU/bodega
    """Genera métricas de stock (negativos, disponibilidad)."""
    if df.empty:
        return {"dataset": "stage_inventory", "registros": 0, "issues": "sin datos"}
    negative_stock = int((df["stock"] < 0).sum())
    return {
        "dataset": "stage_inventory",
        "registros": len(df),
        "negative_stock": negative_stock,
        "detalle": "revisar" if negative_stock else "ok",
    }


@task
def build_quality_report() -> int:
    """Compila hallazgos de DQ en staging y los exporta a tmp/dq_resumen.csv."""
    rows: List[dict] = []
    try:
        orders = read_dataframe("SELECT * FROM stage_ordenes")
    except Exception:  # noqa: BLE001
        orders = pd.DataFrame()
    try:
        items = read_dataframe("SELECT * FROM stage_order_items")
    except Exception:  # noqa: BLE001
        items = pd.DataFrame()
    # Agregados de líneas para validar contra el total de órdenes (monto de ítems).
    items_agg = (
        items.assign(items_amount=items["quantity"] * items["unit_price"])
        .groupby("order_id", as_index=False)["items_amount"]
        .sum()
        if not items.empty
        else pd.DataFrame()
    )
    rows.append(_summarize_orders(orders, items_agg if not items_agg.empty else None))
    valid_orders = set(orders["order_id"]) if not orders.empty else None
    rows.append(_summarize_items(items, valid_orders))

    try:
        payments = read_dataframe("SELECT * FROM stage_payments")
    except Exception:  # noqa: BLE001
        payments = pd.DataFrame()
    rows.append(_summarize_payments(payments))

    try:
        inv = read_dataframe("SELECT * FROM stage_inventory")
    except Exception:  # noqa: BLE001
        inv = pd.DataFrame()
    rows.append(_summarize_inventory(inv))

    df_report = pd.DataFrame(rows)
    # DAMA: Data Quality Monitoring (registro de hallazgos en un artefacto auditable)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    df_report.to_csv(OUTPUT, index=False)
    log_step("DQ", f"Reporte generado en {OUTPUT}")
    return len(df_report)


@flow(name="edu_quality_check_flow")
def run() -> None:
    """Flujo Prefect que genera el reporte DQ y registra la ejecución."""
    try:
        total = build_quality_report.submit().result()
        record_run("dq_revision", "OK", total, f"archivo={OUTPUT.name}")
    except Exception as exc:  # noqa: BLE001
        record_run("dq_revision", "ERROR", 0, str(exc))
        raise


if __name__ == "__main__":
    run()
