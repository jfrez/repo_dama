#!/usr/bin/env python
"""
Carga histórica de catálogo de productos desde CSV a raw_catalogo_csv.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from prefect import flow, task

from utils_edu.db import log_step, record_run, write_dataframe


DEFAULT_CSV = Path(__file__).resolve().parent / "samples" / "catalogo.csv"


@task
def load_csv(path: Path) -> pd.DataFrame:
    """Lee el CSV de catálogo desde la ruta especificada."""
    # DAMA: Data Acquisition (carga batch de catálogo)
    log_step("HIST-CATALOGO", f"Leyendo {path}")
    return pd.read_csv(path)


@task
def normalize(df: pd.DataFrame) -> pd.DataFrame:
    """Tipifica columnas y aplica defaults para precios/activo."""
    # DAMA: Data Quality (tipos, defaults y control de precios)
    log_step("HIST-CATALOGO", "Normalizando columnas")
    expected = ["sku", "nombre", "categoria", "precio", "moneda", "activo", "actualizado_en"]
    for col in expected:
        if col not in df.columns:
            df[col] = None
    # Precios numéricos y flag de activo con default 1 para no reventar cargas con datos incompletos.
    df["precio"] = pd.to_numeric(df["precio"], errors="coerce")
    df["activo"] = df["activo"].fillna(1).astype(int)
    df["actualizado_en"] = pd.to_datetime(df["actualizado_en"], errors="coerce").dt.strftime("%Y-%m-%d")
    return df[expected]


@task
def persist(df: pd.DataFrame) -> int:
    """Persiste el catálogo en raw_catalogo_csv reemplazando datos previos."""
    # DAMA: Data Storage/Operations (capa raw de catálogo)
    write_dataframe(df, "raw_catalogo_csv", if_exists="replace")
    return len(df)


@flow(name="edu_catalogo_initial_flow")
def run(csv_path: str = str(DEFAULT_CSV)) -> None:
    """Flujo Prefect para importar catálogo batch desde CSV."""
    try:
        # 1) Leer fuente
        df = load_csv.submit(Path(csv_path)).result()
        # 2) Normalizar/tipificar valores
        df_norm = normalize.submit(df).result()
        # 3) Persistir en raw con reemplazo total
        inserted = persist.submit(df_norm).result()
        log_step("HIST-CATALOGO", f"Cargados {inserted} productos")
        record_run("historico_catalogo", "OK", inserted, f"Archivo {Path(csv_path).name}")
    except Exception as exc:  # noqa: BLE001
        log_step("HIST-CATALOGO", f"Fallo: {exc}")
        record_run("historico_catalogo", "ERROR", 0, str(exc))
        raise


if __name__ == "__main__":
    run()
