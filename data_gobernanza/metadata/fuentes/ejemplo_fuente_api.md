# Ficha de fuente - API ventas incremental

- Origen: API/fixture `data_01_adquisicion/continuo/ventas/api/fixtures/ventas_incremental.json`
- Formato: JSON; version v1; endpoint simulado local.
- Periodicidad: dos veces al dia; lookback configurable (`EDU_PROGRESSIVE_LOOKBACK_DAYS`, default 7).
- SLA: entrega antes de 06:00 y 18:00; 99% disponibilidad esperada.
- Campos clave: `order_id`, `line_number`, `payment_id`, `sku`, `updated_at`.
- Clasificacion: Interno; contiene PII indirecta en direcciones.
- Responsable: Equipo docente (owner); contacto tutor@demo.edu.
- Retencion: raw 90 dias; registros sobrescritos se conservan por dedupe.
- DQ asociada: ver `../../dq_reglas/ingesta/ejemplo_ordenes_ingesta.md`.
