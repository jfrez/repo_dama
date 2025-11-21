#!/usr/bin/env python
"""
Carga histórica de clientes desde CSV a la tabla raw_clientes_csv.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from prefect import flow, task

from utils_edu.db import log_step, record_run, write_dataframe


DEFAULT_CSV = Path(__file__).resolve().parent / "samples" / "clientes.csv"


@task
def load_csv(path: Path) -> pd.DataFrame:
    """Lee el archivo de clientes desde la ruta indicada."""
    # DAMA: Data Acquisition (ingesta batch de fuente externa)
    log_step("HIST-CLIENTES", f"Leyendo {path}")
    return pd.read_csv(path)


@task
def normalize(df: pd.DataFrame) -> pd.DataFrame:
    """Estandariza columnas y formatea fechas según el diccionario."""
    # DAMA: Data Quality & Data Modeling (estandariza y tipifica columnas)
    log_step("HIST-CLIENTES", "Normalizando columnas")
    expected = ["customer_id", "nombre", "email", "pais", "region", "creado_en", "actualizado_en"]
    for col in expected:
        if col not in df.columns:
            df[col] = None
    # Ajusta fechas al formato estándar del diccionario para consistencia cross-flujos.
    df["creado_en"] = pd.to_datetime(df["creado_en"], errors="coerce").dt.date.astype(str)
    df["actualizado_en"] = pd.to_datetime(df["actualizado_en"], errors="coerce").dt.strftime("%Y-%m-%d")
    return df[expected]


@task
def persist(df: pd.DataFrame) -> int:
    """Escribe el DataFrame en la tabla raw_clientes_csv reemplazando el contenido."""
    # DAMA: Data Storage/Operations (persistencia en capa raw)
    write_dataframe(df, "raw_clientes_csv", if_exists="replace")
    return len(df)


@flow(name="edu_clientes_initial_flow")
def run(csv_path: str = str(DEFAULT_CSV)) -> None:
    """Orquesta la carga inicial de clientes desde CSV hacia la capa raw."""
    try:
        # 1) Leer fuente
        df = load_csv.submit(Path(csv_path)).result()
        # 2) Normalizar y tipificar
        df_norm = normalize.submit(df).result()
        # 3) Persistir a raw + trazabilidad
        inserted = persist.submit(df_norm).result()
        log_step("HIST-CLIENTES", f"Cargados {inserted} clientes")
        record_run("historico_clientes", "OK", inserted, f"Archivo {Path(csv_path).name}")
    except Exception as exc:  # noqa: BLE001
        log_step("HIST-CLIENTES", f"Fallo: {exc}")
        record_run("historico_clientes", "ERROR", 0, str(exc))
        raise


if __name__ == "__main__":
    run()
