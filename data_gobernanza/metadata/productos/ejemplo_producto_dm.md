# Ficha de producto - dm_sales_diarias

- Proposito: medir volumen de ventas diarias por categoria para analisis rapido en el curso.
- Consumidor: alumnos y tutores; canal: CSV `tmp/reporte_ventas.csv` generado por `data_04_usos/reportes/reporte_resumen.py`.
- SLA: frescura diaria antes de 19:30; disponibilidad 99% durante el curso.
- Layout: `fecha (date)`, `categoria (string)`, `ordenes (int)`, `items (int)`, `monto_bruto (decimal)`, `monto_neto (decimal)`, `update_ts (datetime)`.
- Dependencias: `core_ordenes`, `core_order_items`, `stage_catalogo`.
- Controles: ver `../../dq_reglas/consumo/ejemplo_dm.md`; contratistas deben respetar clasificacion "publico interno".
- Retencion: 6 meses.
