# Plantilla de diccionario de datos

Tabla Markdown sugerida para `data_gobernanza/diccionarios/tablas.md`:

| Tabla | Descripción | Campos clave | Periodicidad | Origen | Sensibilidad | Owner | Notas |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `tabla_ejemplo` | Qué contiene y para qué se usa | `pk` (o lista compuesta) | batch inicial / continua / cron | Fuente (CSV/API/tabla) | PII / Sensible / No sensible | Rol/Contacto | Dependencias, lookback, supuestos |

Indicaciones:
- Usa nombres de columnas tal cual en la base.
- Explica granularidad y frecuencia.
- Marca si contiene datos personales y quién es responsable del dominio.
