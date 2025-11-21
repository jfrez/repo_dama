# Reglas DQ - Ingesta de ordenes (raw)

| Regla | Dom | Punto | Umbral | Responsable | Accion |
| --- | --- | --- | --- | --- | --- |
| `order_id` no nulo | Ventas | Ingesta | 0% nulos | Ingenieria | Rechazar registro y log en `tmp/historico/ordenes.log` |
| `total_amount` >= 0 | Ventas | Ingesta | 0 valores negativos | Ingenieria | Marcar registro, enviar alerta si >0.5% |
| Duplicado por (`order_id`,`source`) | Ventas | Ingesta | 0% | Ingenieria | Conservar ultimo por `updated_at`, registrar conteo |

Relacionar con `metadata/fuentes/ejemplo_fuente_api.md` y diccionario `diccionarios/raw/ejemplo_raw_clientes.md`.
