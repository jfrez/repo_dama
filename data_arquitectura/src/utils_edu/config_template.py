"""
Ejemplo de configuración para el proyecto educacional.

Renombra este archivo a `config.py` si quieres centralizar las
credenciales en vez de usar variables de entorno.
"""

CONFIG = {
    # Cadena de conexión SQLAlchemy. Dejar vacío para usar SQLite local.
    "EDU_DB_URL": "postgresql+psycopg2://usuario:clave@localhost:5432/educacional",
    # API real para la carga continua; dejar vacío para usar el fixture.
    "EDU_API_URL": "",
    # Ventana de lookback para la carga incremental (en días).
    "EDU_PROGRESSIVE_LOOKBACK_DAYS": 7,
}
# Plantilla de configuración: DAMA (Data Management & Security) centraliza parámetros sensibles.
# Nota: personalízalo como `config.py` y evita subir credenciales reales al repositorio.
