# Ejemplo de arquitectura y modelado

- Capas: `raw_*` conservan nombres y tipos de origen, `stage_*` usa snake_case y PK claras, `core_*` consolida dominios, `dm_*` expone productos.
- Claves maestras: `customer_id`, `order_id`, `sku` se mantienen constantes; dedupe por `updated_at` en ingestas API.
- Granularidad: `dm_sales_diarias` se expone por fecha y categoria; `dm_pagos_diarios` por fecha, metodo, estado.
- Versionado: cambios incompatibles en stage/core se suffixan con `_v2` y se documentan en diccionarios y linaje.
- Particionado: tablas de salida se particionan por fecha (columna `fecha`) y se mantienen 6 meses.
