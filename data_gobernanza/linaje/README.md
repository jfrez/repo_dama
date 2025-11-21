# Linaje de datos

Centraliza la trazabilidad de origen a destino (raw -> stage -> core -> dm) para cada flujo.

Incluye:
- Mapa de origenes y destinos por proceso (script, dataset, owner) y dependencias externas.
- Transformaciones clave y reglas DQ aplicadas en cada salto.
- Columnas derivadas, parametros de entorno y supuestos que afectan el resultado.
- Enlaces a evidencias de ejecucion en `tmp/` y a monitoreo en `data_03_operacion/`.

Usa la plantilla `../plantillas/linaje.md` y actualiza cada vez que cambie la frecuencia, la logica o la fuente.
