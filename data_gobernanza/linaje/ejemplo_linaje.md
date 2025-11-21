# Linaje ejemplo: flujo de ventas

| Paso | Origen | Destino | Transformaciones | Reglas DQ | Evidencia |
| --- | --- | --- | --- | --- | --- |
| Ingesta historica | `historico/ordenes/csv/samples/` | `raw_ordenes_csv`, `raw_order_items_csv` | Carga CSV; agrega `ingested_at` | Obligatorios y tipos basicos (`dq_reglas/ingesta/`) | Log en `tmp/historico/ordenes.log` |
| Ingesta continua | API fixture `ventas_incremental.json` | `raw_ordenes_api`, `raw_order_items_api` | Filtra `updated_at` > hoy-7 | Lookback y duplicados | `tmp/continuo/ventas.log` |
| Stage | `raw_ordenes_*` | `stage_ordenes`, `stage_order_items` | Dedupe por `order_id` y `line_number` usando mayor `updated_at` | Referencial vs clientes/catalogo | `tmp/dq_resumen.csv` |
| Core | `stage_*` | `core_ordenes`, `core_order_items` | Calcula monto items y marca desvío | Balance de montos | `tmp/dq_resumen.csv` |
| DM | `core_*`, `stage_catalogo` | `dm_sales_diarias`, `dm_pagos_diarios` | Agrega por fecha/categoria y metodo | Completitud por periodo | `tmp/reporte_ventas.csv`, `tmp/reporte_pagos.csv` |
