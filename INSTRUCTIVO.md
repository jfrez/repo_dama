# Instructivo educativo: comercio electrónico

Guía paso a paso para ejecutar el demo, explicando dónde está cada pieza y qué muestra.

## 1. Preparar el entorno
- Instala dependencias del `requirements.txt` de la raíz.
- Instala el paquete de utilidades: `python -m pip install -e educacional/data_arquitectura/src`.
- Crea la base de datos demo (SQLite por defecto): `python educacional/data_arquitectura/src/utils_edu/init_db.py`.
- Variables opcionales: `EDU_DB_URL` (otra base), `EDU_API_MODE` (`offline|online`), `EDU_API_URL`, `EDU_PROGRESSIVE_LOOKBACK_DAYS`.

## 2. Dominios y rutas
- **Clientes (batch)**: `data_01_adquisicion/historico/clientes/csv/`  
  Flujo: `carga_inicial.py` | Datos: `samples/clientes.csv`
- **Catálogo (batch)**: `data_01_adquisicion/historico/catalogo/csv/`  
  Flujo: `carga_inicial.py` | Datos: `samples/catalogo.csv`
- **Órdenes (batch)**: `data_01_adquisicion/historico/ordenes/csv/`  
  Flujo: `carga_inicial.py` | Datos: `samples/ordenes.csv`, `samples/ordenes_items.csv`
- **Ventas (continuo)**: `data_01_adquisicion/continuo/ventas/api/`  
  Flujo: `carga_progresiva.py` | Fixture API: `fixtures/ventas_incremental.json`

## 3. Ejecutar los flujos en orden
1) **Batch (clientes, catálogo, órdenes)**  
   ```bash
   python educacional/data_01_adquisicion/historico/clientes/csv/carga_inicial.py
   python educacional/data_01_adquisicion/historico/catalogo/csv/carga_inicial.py
   python educacional/data_01_adquisicion/historico/ordenes/csv/carga_inicial.py
   ```
   Llena `raw_clientes_csv`, `raw_catalogo_csv`, `raw_ordenes_csv/raw_order_items_csv`.

2) **API incremental (ventas/pagos/inventario)**  
   `python educacional/data_01_adquisicion/continuo/ventas/api/carga_progresiva.py`  
   Llena `raw_ordenes_api`, `raw_order_items_api`, `raw_payments_api`, `raw_inventory_api` (ventana `EDU_PROGRESSIVE_LOOKBACK_DAYS`).

3) **Staging**  
   `python educacional/data_02_integracion/01_construccion/stage_comercio.py`  
   Deduplica y normaliza clientes, catálogo, órdenes, líneas, pagos e inventario.

4) **Revisión DQ**  
   `python educacional/data_02_integracion/02_procesamiento/revision_calidad.py`  
   Genera `tmp/dq_resumen.csv` con hallazgos (nulos, negativos) para órdenes, líneas, pagos e inventario.

5) **Consolidación**  
   `python educacional/data_02_integracion/03_consolidacion/consolidar_modelo.py`  
   Construye `core_ordenes`, `core_order_items`, `dm_sales_diarias`, `dm_pagos_diarios`, `dm_inventario_snapshot`.

6) **Monitoreo y reporte**  
   - `python educacional/data_03_operacion/monitoreo/resumen_ejecuciones.py` → `tmp/monitoreo_resumen.csv`  
   - `python educacional/data_04_usos/reportes/reporte_resumen.py` → `tmp/reporte_ventas.csv` y `tmp/reporte_pagos.csv`

## 4. Puntos didácticos por carpeta
- **data_arquitectura**: DDL versionado y paquete común (`utils_edu`).
- **data_01_adquisicion**: dominios separados y modos (batch vs incremental).
- **data_02_integracion**: staging → calidad → core/datamart.
- **data_03_operacion**: registro de ejecuciones y snapshot operativo.
- **data_04_usos**: producto consumible (reportes CSV).
- **data_gobernanza**: diccionarios, reglas DQ, catálogo; agentes IA para mantenerlos.

## 5. Orquestación (Prefect)
Rutas en `educacional/agents.md`. Ejemplo de deployment continuo:
```bash
prefect deployment build educacional/data_01_adquisicion/continuo/ventas/api/carga_progresiva.py:run \
  -n edu-api-progressive -q default -o deploy_api.yaml
prefect deployment apply deploy_api.yaml
prefect agent start -q default
```

## 6. Cómo extender el demo
- Agrega otro dominio duplicando `historico/<dominio>/...` o `continuo/<dominio>/...`.
- Amplía reglas en `data_gobernanza/dq_reglas/reglas.md` y actualiza el diccionario `data_gobernanza/diccionarios/tablas.md`.
- Si cambias la base destino, ajusta `EDU_DB_URL` y el SQL en `setup/00_demo_schema.sql`.
