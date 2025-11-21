#!/usr/bin/env python
"""
Monitoreo simple de ejecuciones y salidas clave del demo ecommerce.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from utils_edu.db import log_step, read_dataframe


OUTPUT = Path(__file__).resolve().parents[3] / "tmp" / "monitoreo_resumen.csv"


def main() -> None:
    """Genera un snapshot operativo de ejecuciones y volúmenes recientes."""
    # Paso 1: leer bitácora de ejecuciones
    try:
        runs = read_dataframe(
            "SELECT proceso, estado, registros, detalle, ejecutado_en FROM control_ejecuciones ORDER BY id DESC LIMIT 20"
        )
    except Exception:  # noqa: BLE001
        runs = pd.DataFrame()  # Si es la primera corrida, sigue con dataframe vacío.

    # Paso 2: leer productos clave para saber si hay datos recientes
    try:
        ventas = read_dataframe(
            "SELECT fecha, categoria, ingresos FROM dm_sales_diarias ORDER BY fecha DESC"
        )
    except Exception:  # noqa: BLE001
        ventas = pd.DataFrame()

    try:
        pagos = read_dataframe(
            "SELECT fecha, metodo, estado, monto FROM dm_pagos_diarios ORDER BY fecha DESC"
        )
    except Exception:  # noqa: BLE001
        pagos = pd.DataFrame()

    # Resumen compacto que mezcla últimas ejecuciones con volumen reciente de métricas clave.
    summary = {
        "ejecuciones_totales": len(runs),
        "ultimos_procesos": runs.head(5).to_dict(orient="records") if not runs.empty else [],
        "ventas_registros": len(ventas),
        "pagos_registros": len(pagos),
    }
    # DAMA: Data Operations (observabilidad básica de cargas y métricas)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame([summary]).to_csv(OUTPUT, index=False)
    log_step("MONITOREO", f"Resumen guardado en {OUTPUT}")


if __name__ == "__main__":
    main()
