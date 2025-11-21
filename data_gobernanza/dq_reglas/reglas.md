# Reglas de calidad (demo ecommerce)

- **Claves obligatorias**:
  - Órdenes: `order_id`, `customer_id`, `order_date` no nulos.
  - Líneas: `order_id`, `line_number`, `sku` no nulos.
  - Pagos: `payment_id`, `order_id` no nulos.
- **Valores numéricos**:
  - `total_amount`, `unit_price`, `quantity`, `amount`, `stock` deben ser >= 0.
  - En staging, valores negativos se marcan y se registran en `tmp/dq_resumen.csv`.
- **Ventana incremental API**:
  - Solo se cargan registros con `updated_at` dentro de los últimos `EDU_PROGRESSIVE_LOOKBACK_DAYS` días.
- **Consistencia**:
  - Deduplicación por última `updated_at` en claves (`order_id`, `order_id`+`line_number`, `payment_id`, `sku`+`warehouse`).
  - Líneas y pagos deben referenciar órdenes válidas en `stage_ordenes`; los huérfanos se descartan y se registran.
  - Monto de items (`quantity*unit_price`) se compara contra `total_amount`; los desvíos se marcan en el reporte DQ.
- **Trazabilidad**: cada flujo escribe en `control_ejecuciones` con conteo y detalle (incluye modo/cantidad por entidad en las cargas API).
- **Reporte DQ**: `data_02_integracion/02_procesamiento/revision_calidad.py` genera `tmp/dq_resumen.csv` con hallazgos para órdenes, líneas, pagos e inventario.
