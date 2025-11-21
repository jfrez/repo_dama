# Plantillas de interacción (Catalogador)

## Nueva ficha de dataset
```
Actúa como Catalogador de Metadata.
Dataset: <nombre> en <ruta/sql>.
Describe fuente, frecuencia, SLA de frescura, criticidad, sensibilidad, owner/contacto.
Devuelve fila Markdown para catalogo.md y un breve texto de linaje (fuente → capa destino).
```

## Revisión de ficha existente
```
Revisa la entrada de <dataset> en data_gobernanza/metadata/catalogo.md.
Valida frecuencia vs script <ruta>.
Si falta owner o sensibilidad, sugiere completarlo en una línea.
```
