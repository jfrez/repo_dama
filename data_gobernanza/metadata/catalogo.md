# Catálogo de datos (demo)

| Conjunto | Descripción | Fuente | Frecuencia | Responsable |
| --- | --- | --- | --- | --- |
| Clientes | Datos ficticios de clientes online. | `historico/clientes/csv/samples/clientes.csv` | Batch inicial | Equipo docente |
| Catálogo de productos | Productos, categorías y precios. | `historico/catalogo/csv/samples/catalogo.csv` | Batch inicial | Equipo docente |
| Órdenes | Cabecera y líneas de ventas. | CSV histórico y API fixture `continuo/ventas/api/fixtures/ventas_incremental.json` | Batch inicial + continua | Equipo docente |
| Pagos | Autorizaciones y pagos de órdenes. | API/fixture de pagos (incluido en `ventas_incremental.json`) | Continua (lookback 7 días) | Equipo docente |
| Inventario | Stock por SKU y bodega. | API/fixture (incluido en `ventas_incremental.json`) | Continua (lookback 7 días) | Equipo docente |
| Datamarts de ventas/pagos/inventario | Métricas diarias consolidadas. | `stage_*` ecommerce | Tras cada consolidación | Equipo docente |

Notas:
- Usar estos datasets solo con fines educativos; no representan valores reales.
- Ajustar `EDU_DB_URL` si se quiere probar en PostgreSQL en vez de SQLite.
