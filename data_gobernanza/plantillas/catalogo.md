# Plantilla de ficha de catálogo

Tabla sugerida para `data_gobernanza/metadata/catalogo.md`:

| Conjunto | Descripción | Fuente | Frecuencia / SLA | Criticidad | Sensibilidad | Responsable / Contacto | Linaje breve |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Ventas diarias | Métricas de ventas por fecha y categoría | `stage_ordenes`, `stage_order_items`, `stage_catalogo` | Continua; SLA: D+0 08:00 | Alta | No sensible | Equipo docente (correo) | API/CSV → stage → dm_sales_diarias |

Pautas:
- Especifica frecuencia y SLA de frescura.
- Marca criticidad (alta/media/baja) y sensibilidad (PII/Sensible/No sensible).
- Indica owner/contacto y resumen de linaje (de-para).
