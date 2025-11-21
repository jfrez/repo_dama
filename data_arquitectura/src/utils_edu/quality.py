"""Helpers de reglas simples de calidad de datos."""

from __future__ import annotations

from typing import Dict, Iterable, Tuple

import pandas as pd


def apply_quality_rules(
    df: pd.DataFrame,
    required: Iterable[str] = (),
    numeric_bounds: Dict[str, Tuple[float | None, float | None]] | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Aplica reglas básicas:
    - Elimina registros con nulos en columnas obligatorias.
    - Los valores fuera de rango numérico se reemplazan por NULL.

    Retorna (df_limpio, resumen_reglas).

    DAMA: Data Quality — controles mínimos reutilizables.
    """
    numeric_bounds = numeric_bounds or {}
    df_clean = df.copy()
    issues: list[dict[str, int | str]] = []

    for col in required:
        if col not in df_clean.columns:
            issues.append({"regla": f"columna_faltante:{col}", "registros_afectados": len(df_clean)})
            continue
        nulls = df_clean[col].isna().sum()
        if nulls:
            issues.append({"regla": f"nulos_{col}", "registros_afectados": int(nulls)})
            df_clean = df_clean.dropna(subset=[col])

    for col, (min_val, max_val) in numeric_bounds.items():
        if col not in df_clean.columns:
            issues.append({"regla": f"columna_faltante:{col}", "registros_afectados": len(df_clean)})
            continue
        # Mask arrancando en False para marcar solo valores fuera de rango.
        mask = pd.Series([False] * len(df_clean)) if df_clean.empty else pd.Series(False, index=df_clean.index)
        if min_val is not None:
            mask |= df_clean[col] < min_val
        if max_val is not None:
            mask |= df_clean[col] > max_val
        affected = int(mask.sum())
        if affected:
            issues.append({"regla": f"rango_{col}", "registros_afectados": affected})
            df_clean.loc[mask, col] = None

    # El resumen puede quedar vacío; el consumidor decide si trata eso como "sin hallazgos".
    summary = pd.DataFrame(issues)
    return df_clean, summary
