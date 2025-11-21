"""Funciones auxiliares de base de datos para el proyecto educacional."""

from __future__ import annotations

import datetime as dt
import os
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Dict, Iterable, Optional

import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine


DEFAULT_SQLITE_PATH = Path(__file__).resolve().parents[3] / "tmp" / "edu_demo.db"
# Archivo SQLite por defecto cuando no se entrega `EDU_DB_URL` (permite correr el demo sin dependencias externas).


def _ensure_sqlite_dir(path: Path) -> None:
    """Crea el directorio de SQLite si no existe (evita fallos al escribir)."""
    # Crea la carpeta tmp si no existe para evitar fallos de IO en la ruta por defecto.
    path.parent.mkdir(parents=True, exist_ok=True)


def get_engine() -> Engine:
    """Retorna un engine SQLAlchemy. Usa SQLite local si no se define EDU_DB_URL.

    DAMA: Data Architecture/Storage — centraliza la fuente de datos del demo.
    """
    db_url = os.getenv("EDU_DB_URL")
    if not db_url:
        _ensure_sqlite_dir(DEFAULT_SQLITE_PATH)
        db_url = f"sqlite:///{DEFAULT_SQLITE_PATH}"
    return create_engine(db_url, future=True)


@contextmanager
def get_connection():
    """Context manager que abre una conexión transaccional y la cierra al salir."""
    engine = get_engine()
    with engine.begin() as conn:
        yield conn


def run_sql_file(sql_file: Path) -> None:
    """Ejecuta cada sentencia separada por ';' en el archivo SQL.

    DAMA: Data Development — aplica DDL versionado.
    """
    sql_file = Path(sql_file)
    if not sql_file.exists():
        raise FileNotFoundError(sql_file)

    sql_text = sql_file.read_text()
    statements = [stmt.strip() for stmt in sql_text.split(";") if stmt.strip()]
    if not statements:
        return

    with get_connection() as conn:
        for stmt in statements:
            conn.execute(text(stmt))


def read_dataframe(query: str, params: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
    """DAMA: Data Access — lectura controlada vía SQLAlchemy."""
    with get_connection() as conn:
        return pd.read_sql(text(query), conn, params=params)


def write_dataframe(
    df: pd.DataFrame,
    table: str,
    if_exists: str = "append",
    dtype: Optional[Dict[str, Any]] = None,
) -> None:
    """DAMA: Data Operations — inserta DataFrames respetando el modo de escritura."""
    df.to_sql(table, get_engine(), if_exists=if_exists, index=False, dtype=dtype)


def record_run(proceso: str, estado: str, registros: int = 0, detalle: str | None = None) -> None:
    """Registra una corrida en control_ejecuciones con conteo y detalle."""
    payload = pd.DataFrame(
        [
            {
                "proceso": proceso,
                "estado": estado,
                "registros": registros,
                "detalle": detalle or "",
                "ejecutado_en": dt.datetime.now().isoformat(),
            }
        ]
    )
    write_dataframe(payload, "control_ejecuciones")


def log_step(step: str, message: str) -> None:
    """Imprime mensajes breves de trazabilidad en terminal."""
    print(f"[{step}] {message}")
