# Dominio: Órdenes (batch)

- **Objetivo**: cargar órdenes históricas (cabecera y líneas) a `raw_ordenes_csv` y `raw_order_items_csv`.
- **Script/flujo**: `csv/carga_inicial.py` (`edu_ordenes_initial_flow`).
- **Entrada**: `csv/samples/ordenes.csv` y `csv/samples/ordenes_items.csv`.
- **Salida**: inserta en tablas raw y registra en `control_ejecuciones`.

Ejecución:
```bash
python educacional/data_01_adquisicion/historico/ordenes/csv/carga_inicial.py
```
