# Diccionario ejemplo - core_ordenes

| Campo | Tipo | Regla | Sensibilidad | Owner |
| --- | --- | --- | --- | --- |
| order_id | string | PK de orden | Interno | Equipo docente |
| customer_id | string | De `stage_ordenes` | Interno | Equipo docente |
| order_date | date | De `stage_ordenes` | Interno | Equipo docente |
| total_amount | decimal | De `stage_ordenes`; validado vs suma de items | Interno | Equipo docente |
| items_amount | decimal | Sum(`quantity*unit_price`) de `core_order_items` | Interno | Ingenieria |
| amount_diff | decimal | `total_amount - items_amount` | Interno | Ingenieria |
| status | string | De `stage_ordenes` | Interno | Equipo docente |
| updated_at | datetime | Ultima actualizacion consolidada | Interno | Ingenieria |

Reglas: `amount_diff` debe estar dentro de ±0.5; desviaciones se registran en `tmp/dq_resumen.csv`.
