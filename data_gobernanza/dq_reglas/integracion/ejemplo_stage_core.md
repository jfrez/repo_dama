# Reglas DQ - Integracion stage/core

| Regla | Dom | Punto | Umbral | Responsable | Accion |
| --- | --- | --- | --- | --- | --- |
| Referencial `stage_order_items.order_id` en `stage_ordenes` | Ventas | Integracion | 0 huérfanos | Ingenieria | Descartar huérfanos y log en `tmp/dq_resumen.csv` |
| Balance `total_amount` vs suma de items | Ventas | Integracion | |amount_diff| <= 0.5 | Steward | Marcar desvio, revisar manual si > 10 casos |
| Dedupe `payment_id` en `stage_payments` | Pagos | Integracion | 0 duplicados | Ingenieria | Mantener ultimo `updated_at`, registrar conteo |

Ejecucion recomendada: `data_02_integracion/02_procesamiento/revision_calidad.py`.
