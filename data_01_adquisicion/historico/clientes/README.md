# Dominio: Clientes (batch)

- **Objetivo**: cargar clientes desde CSV a `raw_clientes_csv`.
- **Script/flujo**: `csv/carga_inicial.py` (`edu_clientes_initial_flow`).
- **Entrada**: `csv/samples/clientes.csv` (puedes reemplazarlo manteniendo columnas).
- **Salida**: inserta en `raw_clientes_csv` y registra en `control_ejecuciones`.

Ejecución:
```bash
python educacional/data_01_adquisicion/historico/clientes/csv/carga_inicial.py
```
