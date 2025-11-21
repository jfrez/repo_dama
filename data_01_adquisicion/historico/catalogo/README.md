# Dominio: Catálogo (batch)

- **Objetivo**: cargar productos y precios desde CSV a `raw_catalogo_csv`.
- **Script/flujo**: `csv/carga_inicial.py` (`edu_catalogo_initial_flow`).
- **Entrada**: `csv/samples/catalogo.csv`.
- **Salida**: inserta en `raw_catalogo_csv` y registra en `control_ejecuciones`.

Ejecución:
```bash
python educacional/data_01_adquisicion/historico/catalogo/csv/carga_inicial.py
```
