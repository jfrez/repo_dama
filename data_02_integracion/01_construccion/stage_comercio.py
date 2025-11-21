#!/usr/bin/env python
"""
Construcción de staging para comercio electrónico.
Une cargas históricas (CSV) e incrementales (API), aplica reglas mínimas y deja listas las tablas stage.
"""

from __future__ import annotations

import pandas as pd
from prefect import flow, task

from utils_edu.db import log_step, read_dataframe, record_run, write_dataframe
from utils_edu.quality import apply_quality_rules


def _dedupe_latest(df: pd.DataFrame, key_cols: list[str], ts_col: str) -> pd.DataFrame:
    """Deduplica preservando último registro según timestamp para las claves indicadas."""
    # DAMA: Data Quality (deduplicación por última marca de tiempo)
    if df.empty:
        return df
    df = df.sort_values(ts_col).dropna(subset=key_cols)
    return df.drop_duplicates(subset=key_cols, keep="last")


@task
def stage_clientes() -> int:
    """Prepara stage_clientes: limpia, deduplica y escribe la tabla."""
    # Paso 1: leer raw clientes
    try:
        raw = read_dataframe("SELECT * FROM raw_clientes_csv")
    except Exception:  # noqa: BLE001
        raw = pd.DataFrame()
    if raw.empty:
        log_step("STAGE-CLIENTES", "Sin datos")
        return 0
    raw["actualizado_en"] = pd.to_datetime(raw["actualizado_en"], errors="coerce")
    cleaned, summary = apply_quality_rules(raw, required=["customer_id"])
    if not summary.empty:
        log_step("STAGE-CLIENTES", f"Observaciones: {summary.to_dict(orient='records')}")
    cleaned = _dedupe_latest(cleaned, ["customer_id"], "actualizado_en")
    cleaned["actualizado_en"] = cleaned["actualizado_en"].dt.strftime("%Y-%m-%d")
    write_dataframe(cleaned, "stage_clientes", if_exists="replace")
    return len(cleaned)


@task
def stage_catalogo() -> int:
    """Prepara stage_catalogo: tipifica, controla precios y deduplica SKU."""
    # Paso 2: leer raw catálogo
    try:
        raw = read_dataframe("SELECT * FROM raw_catalogo_csv")
    except Exception:  # noqa: BLE001
        raw = pd.DataFrame()
    if raw.empty:
        log_step("STAGE-CATALOGO", "Sin datos")
        return 0
    raw["precio"] = pd.to_numeric(raw["precio"], errors="coerce")
    raw["actualizado_en"] = pd.to_datetime(raw["actualizado_en"], errors="coerce")
    cleaned, summary = apply_quality_rules(raw, required=["sku"], numeric_bounds={"precio": (0, None)})
    if not summary.empty:
        log_step("STAGE-CATALOGO", f"Observaciones: {summary.to_dict(orient='records')}")
    cleaned = _dedupe_latest(cleaned, ["sku"], "actualizado_en")
    cleaned["actualizado_en"] = cleaned["actualizado_en"].dt.strftime("%Y-%m-%d")
    write_dataframe(cleaned, "stage_catalogo", if_exists="replace")
    return len(cleaned)


@task
def stage_ordenes() -> int:
    """Une órdenes CSV+API, aplica controles y deja stage_ordenes."""
    # Paso 3: unir órdenes CSV + API
    try:
        raw_csv = read_dataframe("SELECT *, 'csv' AS source FROM raw_ordenes_csv")
    except Exception:  # noqa: BLE001
        raw_csv = pd.DataFrame()
    try:
        raw_api = read_dataframe("SELECT * FROM raw_ordenes_api")
    except Exception:  # noqa: BLE001
        raw_api = pd.DataFrame()

    # Se concatenan ambas fuentes; si alguna falta se sigue con la disponible.
    combined = pd.concat([raw_csv, raw_api], ignore_index=True) if not raw_csv.empty or not raw_api.empty else pd.DataFrame()
    if combined.empty:
        log_step("STAGE-ORDENES", "Sin datos en raw")
        return 0

    combined["total_amount"] = pd.to_numeric(combined["total_amount"], errors="coerce")
    combined["order_date"] = pd.to_datetime(combined["order_date"], errors="coerce")
    combined["updated_at"] = pd.to_datetime(combined["updated_at"], errors="coerce")

    cleaned, summary = apply_quality_rules(
        combined,
        required=["order_id", "customer_id", "order_date"],
        numeric_bounds={"total_amount": (0, None)},
    )
    if not summary.empty:
        log_step("STAGE-ORDENES", f"Observaciones: {summary.to_dict(orient='records')}")

    cleaned = _dedupe_latest(cleaned, ["order_id"], "updated_at")
    cleaned["order_date"] = cleaned["order_date"].dt.strftime("%Y-%m-%d")
    cleaned["updated_at"] = cleaned["updated_at"].dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    write_dataframe(cleaned, "stage_ordenes", if_exists="replace")
    return len(cleaned)


@task
def stage_order_items() -> int:
    """Une líneas CSV+API, controla datos y mantiene solo órdenes válidas."""
    # Paso 4: unir líneas CSV + API
    try:
        raw_csv = read_dataframe("SELECT *, 'csv' AS source FROM raw_order_items_csv")
    except Exception:  # noqa: BLE001
        raw_csv = pd.DataFrame()
    try:
        raw_api = read_dataframe("SELECT * FROM raw_order_items_api")
    except Exception:  # noqa: BLE001
        raw_api = pd.DataFrame()
    combined = pd.concat([raw_csv, raw_api], ignore_index=True) if not raw_csv.empty or not raw_api.empty else pd.DataFrame()
    if combined.empty:
        log_step("STAGE-ITEMS", "Sin datos en raw")
        return 0

    combined["quantity"] = pd.to_numeric(combined["quantity"], errors="coerce").fillna(0).astype(int)
    combined["unit_price"] = pd.to_numeric(combined["unit_price"], errors="coerce")
    combined["updated_at"] = pd.to_datetime(combined["updated_at"], errors="coerce")

    cleaned, summary = apply_quality_rules(
        combined,
        required=["order_id", "line_number", "sku"],
        numeric_bounds={"quantity": (0, None), "unit_price": (0, None)},
    )
    if not summary.empty:
        log_step("STAGE-ITEMS", f"Observaciones: {summary.to_dict(orient='records')}")

    cleaned = _dedupe_latest(cleaned, ["order_id", "line_number"], "updated_at")
    # Filtra solo líneas con orden válida en stage_ordenes para evitar huérfanos.
    try:
        valid_orders_df = read_dataframe("SELECT order_id FROM stage_ordenes")
    except Exception:  # noqa: BLE001
        valid_orders_df = pd.DataFrame()
    if valid_orders_df.empty:
        log_step("STAGE-ITEMS", "Sin stage_ordenes; se omiten líneas")
        return 0
    valid_orders = set(valid_orders_df["order_id"])
    before = len(cleaned)
    cleaned = cleaned[cleaned["order_id"].isin(valid_orders)]
    dropped = before - len(cleaned)
    if dropped:
        log_step("STAGE-ITEMS", f"Descartadas {dropped} líneas sin orden en stage_ordenes")
    cleaned["updated_at"] = cleaned["updated_at"].dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    write_dataframe(cleaned, "stage_order_items", if_exists="replace")
    return len(cleaned)


@task
def stage_payments() -> int:
    """Normaliza pagos API, deduplica y filtra contra órdenes válidas."""
    # Paso 5: pagos (solo API)
    try:
        raw = read_dataframe("SELECT * FROM raw_payments_api")
    except Exception:  # noqa: BLE001
        raw = pd.DataFrame()
    if raw.empty:
        log_step("STAGE-PAYMENTS", "Sin datos en raw_payments_api")
        return 0
    raw["amount"] = pd.to_numeric(raw["amount"], errors="coerce")
    raw["paid_at"] = pd.to_datetime(raw["paid_at"], errors="coerce")
    raw["updated_at"] = pd.to_datetime(raw["updated_at"], errors="coerce")
    cleaned, summary = apply_quality_rules(
        raw,
        required=["payment_id", "order_id"],
        numeric_bounds={"amount": (0, None)},
    )
    if not summary.empty:
        log_step("STAGE-PAYMENTS", f"Observaciones: {summary.to_dict(orient='records')}")
    cleaned = _dedupe_latest(cleaned, ["payment_id"], "updated_at")
    # Mantén solo pagos asociados a órdenes ya aceptadas en stage_ordenes.
    try:
        valid_orders_df = read_dataframe("SELECT order_id FROM stage_ordenes")
    except Exception:  # noqa: BLE001
        valid_orders_df = pd.DataFrame()
    if valid_orders_df.empty:
        log_step("STAGE-PAYMENTS", "Sin stage_ordenes; se omiten pagos")
        return 0
    valid_orders = set(valid_orders_df["order_id"])
    before = len(cleaned)
    cleaned = cleaned[cleaned["order_id"].isin(valid_orders)]
    dropped = before - len(cleaned)
    if dropped:
        log_step("STAGE-PAYMENTS", f"Descartados {dropped} pagos sin orden en stage_ordenes")
    cleaned["paid_at"] = cleaned["paid_at"].dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    cleaned["updated_at"] = cleaned["updated_at"].dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    write_dataframe(cleaned, "stage_payments", if_exists="replace")
    return len(cleaned)


@task
def stage_inventory() -> int:
    """Normaliza y deduplica inventario API en stage_inventory."""
    # Paso 6: inventario (solo API)
    try:
        raw = read_dataframe("SELECT * FROM raw_inventory_api")
    except Exception:  # noqa: BLE001
        raw = pd.DataFrame()
    if raw.empty:
        log_step("STAGE-INVENTORY", "Sin datos en raw_inventory_api")
        return 0
    raw["stock"] = pd.to_numeric(raw["stock"], errors="coerce").fillna(0).astype(int)
    raw["updated_at"] = pd.to_datetime(raw["updated_at"], errors="coerce")
    cleaned, summary = apply_quality_rules(raw, required=["sku", "warehouse"], numeric_bounds={"stock": (0, None)})
    if not summary.empty:
        log_step("STAGE-INVENTORY", f"Observaciones: {summary.to_dict(orient='records')}")
    cleaned = _dedupe_latest(cleaned, ["sku", "warehouse"], "updated_at")
    cleaned["updated_at"] = cleaned["updated_at"].dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    write_dataframe(cleaned, "stage_inventory", if_exists="replace")
    return len(cleaned)


@flow(name="edu_stage_build_flow")
def run() -> None:
    """Orquesta la construcción completa de staging para el dominio ecommerce."""
    try:
        counts = {
            "clientes": stage_clientes.submit().result(),
            "catalogo": stage_catalogo.submit().result(),
            "ordenes": stage_ordenes.submit().result(),
            "items": stage_order_items.submit().result(),
            "payments": stage_payments.submit().result(),
            "inventory": stage_inventory.submit().result(),
        }
        total = sum(counts.values())
        record_run("stage_build", "OK", total, f"detalles={counts}")
    except Exception as exc:  # noqa: BLE001
        record_run("stage_build", "ERROR", 0, str(exc))
        raise


if __name__ == "__main__":
    run()
