# Convenciones para documentar linaje

- Describe siempre capa origen y capa destino (raw/stage/core/dm/tmp).
- Incluye transformaciones clave: cálculos, deduplicaciones, filtros (lookback).
- Menciona dependencias temporales: orden de ejecución, SLA, colas Prefect.
- Señala si se arrastran datos sensibles y en qué columna.
- Usa nombres de tablas/columnas tal cual están en código SQL/Python.
