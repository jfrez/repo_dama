#!/usr/bin/env python
"""
Genera un reporte sencillo de ventas por categoría y pagos por método.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from utils_edu.db import log_step, read_dataframe


DEST_SALES = Path(__file__).resolve().parents[3] / "tmp" / "reporte_ventas.csv"
DEST_PAGOS = Path(__file__).resolve().parents[3] / "tmp" / "reporte_pagos.csv"


def export_sales() -> int:
    # DAMA: Data Delivery — ventas agregadas listas para consumo liviano
    """Crea un CSV de ventas pivotado por fecha y categoría."""
    try:
        dm = read_dataframe("SELECT * FROM dm_sales_diarias")
    except Exception:  # noqa: BLE001
        dm = pd.DataFrame()
    if dm.empty:
        log_step("REPORTE", "dm_sales_diarias vacío; ejecuta consolidación primero.")
        return 0
    # Pivot para dejar montos por categoría en columnas (formato amigable a analistas/CSV).
    pivot = (
        dm.pivot_table(index="fecha", columns="categoria", values="ingresos", aggfunc="sum")
        .reset_index()
        .sort_values("fecha")
    )
    DEST_SALES.parent.mkdir(parents=True, exist_ok=True)
    pivot.to_csv(DEST_SALES, index=False)
    log_step("REPORTE", f"Exportado resumen ventas en {DEST_SALES}")
    return len(pivot)


def export_pagos() -> int:
    # DAMA: Data Delivery — detalle de pagos por método/estado
    """Exporta pagos agrupados a CSV ordenado para consumo analítico."""
    try:
        dm = read_dataframe("SELECT * FROM dm_pagos_diarios")
    except Exception:  # noqa: BLE001
        dm = pd.DataFrame()
    if dm.empty:
        return 0
    # Ordena para que el CSV mantenga estabilidad al compararse entre ejecuciones.
    dm = dm.sort_values(["fecha", "metodo", "estado"])
    # DAMA: Data Delivery (reportes listos para consumo analítico)
    DEST_PAGOS.parent.mkdir(parents=True, exist_ok=True)
    dm.to_csv(DEST_PAGOS, index=False)
    log_step("REPORTE", f"Exportado resumen pagos en {DEST_PAGOS}")
    return len(dm)


def main() -> None:
    """Ejecuta las exportaciones de ventas y pagos a la carpeta tmp/."""
    # Paso: exportar ventas y pagos a CSV listos para consumo
    export_sales()
    export_pagos()


if __name__ == "__main__":
    main()
