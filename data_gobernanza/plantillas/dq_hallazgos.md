# Plantilla de hallazgos de calidad

Formato de tabla para registrar issues en `tmp/dq_resumen.csv` o en actas de seguimiento:

| Dataset | Regla / control | Severidad (alta/media/baja) | Registros afectados | Acción recomendada | Responsable | Fecha objetivo | Estado |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `stage_ordenes` | Clave customer_id no nula | Alta | 12 | Corregir fuente y reprocesar carga del día | Data Engineer | 2024-05-10 | Abierto |

Recomendaciones:
- Enlaza cada hallazgo con la regla en `data_gobernanza/dq_reglas/reglas.md`.
- Incluye acción concreta (reproceso, corrección de fuente, ajuste de regla).
- Define responsable y fecha para cerrar la brecha.
