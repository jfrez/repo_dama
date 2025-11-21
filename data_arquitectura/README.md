# Arquitectura del demo

- **setup/**: SQL autocontenido para crear tablas del ejercicio (sin dependencias externas).
- **src/**: paquete `utils_edu` con helpers de conexión (SQLite por defecto), calidad y logging.

Uso rápido:
```bash
python -m pip install -e educacional/data_arquitectura/src
python educacional/data_arquitectura/src/utils_edu/init_db.py
```

Si quieres usar PostgreSQL, exporta `EDU_DB_URL` con la cadena de conexión antes de correr los scripts.
