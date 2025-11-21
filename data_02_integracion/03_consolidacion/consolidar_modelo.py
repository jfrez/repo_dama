#!/usr/bin/env python
"""
Consolidación del modelo ecommerce: core de órdenes y datamarts de ventas, pagos e inventario.
"""

from __future__ import annotations

import pandas as pd
from prefect import flow, task

from utils_edu.db import log_step, read_dataframe, record_run, write_dataframe


@task
def build_core_ordenes() -> int:
    # DAMA: Data Integration (core unifica órdenes con monto de ítems)
    """Crea core_ordenes, agregando monto de ítems para control de consistencia."""
    orders = read_dataframe("SELECT * FROM stage_ordenes")
    if orders.empty:
        log_step("CONSOLIDACION", "No hay datos en stage_ordenes")
        return 0
    # Paso: sumar montos de líneas para comparar con totales de orden
    try:
        items = read_dataframe("SELECT order_id, quantity, unit_price FROM stage_order_items")
    except Exception:  # noqa: BLE001
        items = pd.DataFrame()
    if not items.empty:
        items["items_amount"] = items["quantity"] * items["unit_price"]
        totals = items.groupby("order_id", as_index=False)["items_amount"].sum()
        orders = orders.merge(totals, on="order_id", how="left")
    else:
        orders["items_amount"] = None
    write_dataframe(orders, "core_ordenes", if_exists="replace")
    return len(orders)


@task
def build_core_order_items() -> int:
    # DAMA: Data Integration (core de líneas)
    """Publica las líneas consolidadas en core_order_items."""
    try:
        items = read_dataframe("SELECT * FROM stage_order_items")
    except Exception:  # noqa: BLE001
        items = pd.DataFrame()
    if items.empty:
        log_step("CONSOLIDACION", "No hay items en stage_order_items")
        return 0
    write_dataframe(items, "core_order_items", if_exists="replace")
    return len(items)


@task
def build_dm_sales() -> int:
    # DAMA: Data Warehousing (hecho de ventas diarias)
    """Genera dm_sales_diarias agregando órdenes e ítems por fecha/categoría."""
    try:
        orders = read_dataframe("SELECT order_id, order_date FROM stage_ordenes")
        items = read_dataframe("SELECT * FROM stage_order_items")
    except Exception:  # noqa: BLE001
        return 0
    if orders.empty or items.empty:
        log_step("DM-SALES", "Sin datos suficientes (órdenes o items)")
        return 0
    # Paso: enriquecer líneas con catálogo para tener categoría
    items["ingresos"] = items["quantity"] * items["unit_price"]
    fact = items.merge(orders, on="order_id", how="left")
    try:
        catalog = read_dataframe("SELECT sku, categoria FROM stage_catalogo")
    except Exception:  # noqa: BLE001
        catalog = pd.DataFrame()
    if not catalog.empty:
        fact = fact.merge(catalog, on="sku", how="left")
    fact["categoria"] = fact["categoria"].fillna("SIN_CATEGORIA")
    dm = (
        fact.groupby(["order_date", "categoria"], as_index=False)
        .agg(
            total_ordenes=("order_id", "nunique"),
            total_items=("quantity", "sum"),
            ingresos=("ingresos", "sum"),
        )
        .rename(columns={"order_date": "fecha"})
    )
    write_dataframe(dm, "dm_sales_diarias", if_exists="replace")
    return len(dm)


@task
def build_dm_pagos() -> int:
    # DAMA: Data Warehousing (hecho de pagos diarios)
    """Construye dm_pagos_diarios agrupando pagos por fecha/método/estado."""
    try:
        payments = read_dataframe("SELECT * FROM stage_payments")
    except Exception:  # noqa: BLE001
        payments = pd.DataFrame()
    if payments.empty:
        log_step("DM-PAGOS", "Sin datos en stage_payments")
        return 0
    # Usa paid_at cuando existe y cae al updated_at para no perder registros fallidos en línea de tiempo.
    payments["fecha"] = pd.to_datetime(payments["paid_at"].fillna(payments["updated_at"])).dt.strftime("%Y-%m-%d")
    dm = (
        payments.groupby(["fecha", "method", "status"], as_index=False)
        .agg(monto=("amount", "sum"), pagos=("payment_id", "count"))
    )
    write_dataframe(dm, "dm_pagos_diarios", if_exists="replace")
    return len(dm)


@task
def build_dm_inventario() -> int:
    # DAMA: Data Warehousing (snapshot de inventario)
    """Crea dm_inventario_snapshot con stock por fecha/sku/bodega."""
    try:
        inv = read_dataframe("SELECT * FROM stage_inventory")
    except Exception:  # noqa: BLE001
        inv = pd.DataFrame()
    if inv.empty:
        log_step("DM-INVENTARIO", "Sin datos en stage_inventory")
        return 0
    inv["fecha"] = pd.to_datetime(inv["updated_at"]).dt.strftime("%Y-%m-%d")
    dm = inv[["fecha", "sku", "warehouse", "stock"]]
    write_dataframe(dm, "dm_inventario_snapshot", if_exists="replace")
    return len(dm)


@flow(name="edu_consolidation_flow")
def run() -> None:
    """Flujo de consolidación completo: core + datamarts y trazabilidad."""
    try:
        core_orders = build_core_ordenes.submit().result()
        core_items = build_core_order_items.submit().result()
        dm_sales = build_dm_sales.submit().result()
        dm_payments = build_dm_pagos.submit().result()
        dm_inventory = build_dm_inventario.submit().result()
        detail = f"core_orders={core_orders}, core_items={core_items}, dm_sales={dm_sales}, dm_pagos={dm_payments}, dm_inv={dm_inventory}"
        record_run("consolidacion", "OK", core_orders + core_items + dm_sales + dm_payments + dm_inventory, detail)
        log_step("CONSOLIDACION", detail)
    except Exception as exc:  # noqa: BLE001
        record_run("consolidacion", "ERROR", 0, str(exc))
        raise


if __name__ == "__main__":
    run()
