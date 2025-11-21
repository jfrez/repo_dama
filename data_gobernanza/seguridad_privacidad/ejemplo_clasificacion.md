# Ejemplo de seguridad y privacidad

| Dataset | Clasificacion | Campos sensibles | Control | Retencion | Responsable |
| --- | --- | --- | --- | --- | --- |
| `raw_clientes_csv` | Confidencial | `email`, `phone` | Enmascarar en vistas de soporte; acceso solo rol "docente" | 90 dias en raw | Data Owner ventas |
| `stage_ordenes` | Interno | `shipping_address` | Ocultar en datamarts; se mantiene solo en core | 180 dias | Steward ecommerce |
| `dm_sales_diarias` | Publico interno | Ninguno | Acceso de solo lectura a alumnos; sin PII | 180 dias | Equipo docente |

Riesgo abierto: revisar si `payment_method` requiere mascaras al exponer en reportes; pendiente decision en proxima revision mensual.
