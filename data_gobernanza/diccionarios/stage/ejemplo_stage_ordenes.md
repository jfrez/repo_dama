# Diccionario ejemplo - stage_ordenes

| Campo | Tipo | Origen/Regla | Sensibilidad | Owner |
| --- | --- | --- | --- | --- |
| order_id | string | Coalesce de `raw_ordenes_csv/api`; dedupe por max `updated_at` | Interno | Equipo docente |
| customer_id | string | Arrastra de raw | Interno | Equipo docente |
| order_date | date | Parseo de fecha; timezone UTC | Interno | Equipo docente |
| status | string | Normalizado a minusculas | Interno | Equipo docente |
| total_amount | decimal | Como en raw; valida >= 0 | Interno | Equipo docente |
| source | string | Marca `csv` o `api` | Interno | Ingenieria |
| updated_at | datetime | Mayor `updated_at` por `order_id` | Interno | Ingenieria |

PK: `order_id`. Referencias: `customer_id` debe existir en `stage_clientes` (ver `dq_reglas/integracion/`).
