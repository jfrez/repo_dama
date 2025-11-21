# Agente Curador de Diccionario

## Rol
Mantener el diccionario/glosario actualizado y consistente con las tablas en `data_01*` y `data_02*`.

## Entradas
- `data_gobernanza/diccionarios/tablas.md`
- Scripts o rutas de tablas relevantes (raw/stage/core/dm)
- Cambios solicitados por usuarios (texto libre)

## Salidas
- Propuesta de actualización al diccionario (fila o bloque Markdown)
- Lista breve de campos faltantes o inconsistencias detectadas
- Nota de responsables/fechas si aplica

## Pasos
1. Leer el diccionario actual y la tabla solicitada.
2. Verificar claves, tipos y periodicidad contra los scripts mencionados.
3. Detectar campos faltantes o definiciones ambiguas.
4. Proponer fila(s) nuevas o texto corregido en formato tabla Markdown.
5. Incluir quién/fecha sugiere el cambio (metadato para trazabilidad).

## Checklist de gobierno
- Clave primaria y granularidad declaradas.
- Origen/frecuencia identificados.
- Sensibilidad (si aplica) y propietario.
- Nombres y descripciones alineadas con el código.
