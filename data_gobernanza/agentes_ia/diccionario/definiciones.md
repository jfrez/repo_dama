# Definiciones y convenciones (Curador)

- Tabla: nombre exacto en la base (respetar mayúsculas/minúsculas tal como en SQL).
- Descripción: acción y dominio; ejemplo: "Órdenes consolidadas con monto de ítems".
- Campos clave: PK natural o surrogate según se usa; si es compuesta, listar en orden.
- Periodicidad: batch inicial, continua (indicar lookback), o frecuencia en cron.
- Origen: ruta o fuente (CSV, API, stage), con capa mencionada.
- Sensibilidad: si contiene datos personales, marcarlo explícitamente.
- Propietario: rol/responsable del dominio (ej. Equipo docente) y contacto opcional.
