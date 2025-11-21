# Plantilla de linaje de datos

Estructura breve para documentar flujos y dependencias:

- **Flujo**: `<ruta/script>` (nombre Prefect si aplica).
- **Fuentes**: tablas/archivos/API de entrada (capa raw/stage).
- **Transformaciones clave**: cálculos, deduplicaciones, filtros (ej. lookback).
- **Destinos**: tablas o productos generados (stage/core/dm/tmp).
- **Columnas calculadas**: `columna = expresión` (lista).
- **Dependencias temporales**: orden de ejecución, SLA, colas.
- **Sensibilidad**: PII/Sensible/No sensible y cómo se maneja.

Ejemplo:
- Flujo: `data_02_integracion/03_consolidacion/consolidar_modelo.py` (`edu_consolidation_flow`)
- Fuentes: `stage_ordenes`, `stage_order_items`, `stage_payments`, `stage_inventory`, `stage_catalogo`
- Transformaciones: suma de `items_amount`, agregados diarios de ventas/pagos, snapshot inventario
- Destinos: `core_ordenes`, `core_order_items`, `dm_sales_diarias`, `dm_pagos_diarios`, `dm_inventario_snapshot`
- Columnas calculadas: `items_amount = quantity*unit_price`, `ingresos = quantity*unit_price`
- Dependencias: correr después de stage y revisión DQ; SLA D+0 08:00
- Sensibilidad: sin PII (solo IDs de órdenes/SKU)
