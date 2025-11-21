# Ingesta (data_01_adquisicion)

Estructura organizada por **dominio ecommerce** y **modo de carga** (batch vs incremental).

- `historico/clientes/csv/`: carga clientes (CSV).
- `historico/catalogo/csv/`: carga catálogo de productos (CSV).
- `historico/ordenes/csv/`: carga órdenes históricas (cabecera + líneas).
  - Cada carpeta contiene `carga_inicial.py` y `samples/`.
- `continuo/ventas/api/`: incrementales desde API/fixture para órdenes, pagos e inventario.
  - `carga_progresiva.py` y `fixtures/ventas_incremental.json`.

Cada flujo escribe en tablas raw correspondientes y registra la ejecución en `control_ejecuciones`. Ajusta `EDU_PROGRESSIVE_LOOKBACK_DAYS` para la ventana del API.
