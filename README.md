# Proyecto educacional de gestión de datos

Conjunto demostrativo que replica una estructura DAMA-DMBOK, pero con datos ficticios y procesos simples de comercio electrónico. Sirve para enseñar cómo organizar ETL, gobernanza y agentes de orquestación sin depender de fuentes sensibles.

## Qué incluye
- **Arquitectura**: un paquete liviano (`utils_edu`) y SQL de ejemplo para crear una base SQLite (o la que definas vía `EDU_DB_URL`).
- **Ingesta**: cargas histórica desde CSV y continua desde un “API” (puede usar el fixture local).
- **Integración**: etapas de staging, validación de calidad y consolidación a un modelo tipo datamart.
- **Gobernanza**: glosario/diccionario, reglas DQ y agentes de apoyo para documentar y monitorear.
- **Orquestación**: scripts listos para Prefect (deploys sugeridos en `educacional/agents.md`).

## Inicio rápido
1) Instala dependencias (usa las mismas de `requirements.txt`).  
2) Instala el paquete educativo:
```bash
python -m pip install -e educacional/data_arquitectura/src
```
3) Crea la base demo (SQLite por defecto en `educacional/tmp/edu_demo.db`):
```bash
python educacional/data_arquitectura/src/utils_edu/init_db.py
```
4) Ejecuta los ETL:
```bash
# Cargas históricas (clientes, catálogo, órdenes)
python educacional/data_01_adquisicion/historico/clientes/csv/carga_inicial.py
python educacional/data_01_adquisicion/historico/catalogo/csv/carga_inicial.py
python educacional/data_01_adquisicion/historico/ordenes/csv/carga_inicial.py
# Carga continua (órdenes/pagos/inventario via API o fixture)
python educacional/data_01_adquisicion/continuo/ventas/api/carga_progresiva.py
# Consolidación y reglas de calidad
python educacional/data_02_integracion/03_consolidacion/consolidar_modelo.py
```
5) Revisa la documentación de gobernanza en `educacional/data_gobernanza/` y los despliegues/agentes en `educacional/agents.md`.

## Estructura (demo)
```
educacional/
├── data_arquitectura/            # SQL y paquete de soporte
├── data_01_adquisicion/          # Ingesta histórica y continua por dominio ecommerce
│   ├── historico/clientes/csv
│   ├── historico/catalogo/csv
│   ├── historico/ordenes/csv
│   └── continuo/ventas/api
├── data_02_integracion/          # Staging, calidad y consolidación
├── data_03_operacion/            # Monitoreo operativo
├── data_04_usos/                 # Reportes y consumos
└── data_gobernanza/              # Diccionarios, reglas y agentes de IA
```

## Variables de entorno clave
- `EDU_DB_URL`: URL SQLAlchemy de la base de demo. Si no se define, se usa SQLite local.
- `EDU_API_URL`: API real para la carga continua (opcional).  
- `EDU_API_MODE`: `offline` (default, usa fixture JSON) o `online`.  
- `EDU_PROGRESSIVE_LOOKBACK_DAYS`: ventana de sincronización incremental (por defecto 7).

Mantén sincronizados los diccionarios y reglas de `data_gobernanza` cada vez que agregues o ajustes una tabla en los pipelines de ejemplo.

Para una guía paso a paso consulta `educacional/INSTRUCTIVO.md`.
