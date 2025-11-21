# Plantillas de interacción (Documentador de linaje)

## Resumen de linaje por flujo
```
Actúa como Documentador de Linaje.
Flujo: <ruta_del_script>.
Describe en 6 líneas: fuentes, transformaciones clave, tablas destino, columnas calculadas, dependencias temporales, sensibilidad.
Formato: viñetas breves.
```

## Mapa columna a columna
```
Para la tabla <tabla_destino> generada en <ruta_script>:
- Lista columnas y origen (tabla/columna)
- Marca calculadas y fórmula
- Nota si arrastra PII o datos sensibles
Devuelve en tabla Markdown simple.
```
