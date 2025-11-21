# Diccionario ejemplo - dm_sales_diarias

| Campo | Tipo | Definicion | Sensibilidad | Owner |
| --- | --- | --- | --- | --- |
| fecha | date | Fecha de la orden | Publico interno | Equipo docente |
| categoria | string | Categoria del producto (de `stage_catalogo`) | Publico interno | Equipo docente |
| ordenes | int | Conteo de ordenes distintas | Publico interno | Equipo docente |
| items | int | Conteo de lineas | Publico interno | Equipo docente |
| monto_bruto | decimal | Suma de `quantity*unit_price` | Publico interno | Equipo docente |
| monto_neto | decimal | Igual a `monto_bruto` (no hay descuentos) | Publico interno | Equipo docente |
| update_ts | datetime | Timestamp de generacion del dm | Publico interno | Ingenieria |

SLA: disponible diariamente antes de 19:30 (ver `operacion_continuidad/ejemplo_runbook.md`).
