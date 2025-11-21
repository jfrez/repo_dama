# Diccionario de tablas (demo ecommerce)

| Tabla | Descripción | Campos clave | Periodicidad | Origen |
| --- | --- | --- | --- | --- |
| `raw_clientes_csv` | Clientes históricos desde CSV. | `customer_id` | Batch inicial | Archivo `historico/clientes/csv/samples/clientes.csv` |
| `raw_catalogo_csv` | Catálogo de productos desde CSV. | `sku` | Batch inicial | Archivo `historico/catalogo/csv/samples/catalogo.csv` |
| `raw_ordenes_csv` | Cabecera de órdenes históricas. | `order_id` | Batch inicial | Archivo `historico/ordenes/csv/samples/ordenes.csv` |
| `raw_order_items_csv` | Líneas de órdenes históricas. | (`order_id`,`line_number`) | Batch inicial | Archivo `historico/ordenes/csv/samples/ordenes_items.csv` |
| `raw_ordenes_api` | Órdenes recientes desde API/fixture. | `order_id` | Continua (lookback) | `EDU_API_URL` o fixture `continuo/ventas/api/fixtures/ventas_incremental.json` |
| `raw_order_items_api` | Líneas recientes de órdenes. | (`order_id`,`line_number`) | Continua | API/fixture |
| `raw_payments_api` | Pagos asociados a órdenes recientes. | `payment_id` | Continua | API/fixture |
| `raw_inventory_api` | Stock por SKU/bodega reciente. | (`sku`,`warehouse`) | Continua | API/fixture |
| `stage_clientes` | Clientes deduplicados. | `customer_id` | Tras ingesta | `raw_clientes_csv` |
| `stage_catalogo` | Productos deduplicados. | `sku` | Tras ingesta | `raw_catalogo_csv` |
| `stage_ordenes` | Órdenes unificadas CSV+API. | `order_id` | Tras ingesta | `raw_ordenes_*` |
| `stage_order_items` | Líneas unificadas CSV+API. | (`order_id`,`line_number`) | Tras ingesta | `raw_order_items_*` |
| `stage_payments` | Pagos limpios y deduplicados. | `payment_id` | Tras ingesta | `raw_payments_api` |
| `stage_inventory` | Stock consolidado por última actualización. | (`sku`,`warehouse`) | Tras ingesta | `raw_inventory_api` |
| `core_ordenes` | Órdenes consolidadas con monto de items. | `order_id` | Tras consolidación | `stage_ordenes`, `stage_order_items` |
| `core_order_items` | Detalle de items consolidado. | (`order_id`,`line_number`) | Tras consolidación | `stage_order_items` |
| `dm_sales_diarias` | Ventas diarias por categoría. | `fecha`, `categoria` | Tras consolidación | `stage_ordenes`, `stage_order_items`, `stage_catalogo` |
| `dm_pagos_diarios` | Pagos por fecha, método y estado. | `fecha`, `metodo`, `estado` | Tras consolidación | `stage_payments` |
| `dm_inventario_snapshot` | Stock diario por SKU y bodega. | `fecha`, `sku`, `warehouse` | Tras consolidación | `stage_inventory` |
| `control_ejecuciones` | Registro de ejecuciones de los pipelines. | `proceso`, `estado`, `ejecutado_en` | En cada flujo Prefect | Todos los procesos |
