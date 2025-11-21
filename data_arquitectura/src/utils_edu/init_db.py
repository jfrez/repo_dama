"""Crea la base educativa aplicando el SQL de setup."""

from __future__ import annotations

from pathlib import Path

from utils_edu.db import DEFAULT_SQLITE_PATH, log_step, run_sql_file


def main() -> None:
    """Aplica el DDL del demo para inicializar la base educativa."""
    sql_path = Path(__file__).resolve().parents[2] / "setup" / "00_demo_schema.sql"
    # Carga el DDL versionado desde /setup para mantener la demo reproducible.
    log_step("SETUP", f"Aplicando {sql_path.name}...")
    # DAMA: Data Development — creación inicial de estructuras.
    run_sql_file(sql_path)
    log_step("SETUP", f"Base lista en {DEFAULT_SQLITE_PATH}")


if __name__ == "__main__":
    main()
