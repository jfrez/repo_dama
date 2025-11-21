# Reglas DQ - Consumo (dm/reportes)

| Regla | Producto | Punto | Umbral | Responsable | Accion |
| --- | --- | --- | --- | --- | --- |
| Completitud diaria `dm_sales_diarias` | Ventas | Consumo | 100% dias con datos de ultimo mes | Steward | Si falta fecha, reprocesar y alertar | 
| Coherencia vs core (`monto_bruto` = suma core items por fecha/categoria) | Ventas | Consumo | 0.2% tolerancia | Ingenieria | Registrar desvio y bloquear publicacion si >0.5% |
| Layout `tmp/reporte_ventas.csv` coincide con contrato | Ventas | Consumo | 0 columnas faltantes | Ingenieria | Falla el pipeline y se notifica a owner |

Ver contrato en `metadata/productos/ejemplo_producto_dm.md`.
