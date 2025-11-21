# Ejemplo de operacion y continuidad

- Calendario: ingesta historica (una vez); ingesta continua API a las 6:00 y 18:00; consolidacion + reportes a las 19:00.
- SLA: ingesta continua ≤ 30 min; consolidacion ≤ 20 min; reportes disponibles antes de 19:30.
- Monitoreo: `data_03_operacion/monitoreo/resumen_ejecuciones.py` genera `tmp/monitoreo_resumen.csv` con filas leidas/escritas y estado.
- Reproceso: ante fallo de API, reintentar con lookback 2 dias (`EDU_PROGRESSIVE_LOOKBACK_DAYS=2`); si persiste, cargar fixture local y registrar brecha en `dq_reglas/`.
- Dependencias: variables `EDU_API_URL`, `EDU_DB_URL`; credenciales se cargan por entorno. Contacto soporte: tutor@demo.edu.
