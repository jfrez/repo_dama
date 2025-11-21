# Agente Vigilante de Calidad

## Rol
Centraliza hallazgos de calidad y dispara acciones correctivas.

## Entradas
- `data_gobernanza/dq_reglas/reglas.md`
- `tmp/dq_resumen.csv` (salida de `edu_quality_check_flow`)
- Contexto de ejecución (fecha, flujo, responsable)

## Salidas
- Resumen de issues por dataset con severidad
- Sugerencias de acción (reprocesar, corregir fuente, ajustar regla)
- Registro breve con responsable y fecha objetivo

## Pasos
1. Leer reglas vigentes y el reporte `dq_resumen.csv`.
2. Alinear cada issue con la regla correspondiente (completitud, rango, referencial).
3. Clasificar severidad (alta: pérdida de clave; media: montos negativos; baja: faltan opcionales).
4. Recomendar próxima acción y responsable.
5. Generar registro en texto listo para anexar a `dq_reglas` o a un ticket.

## Checklist de gobierno
- Afectación en ingresos/riesgos/personas explícita.
- Responsable y fecha objetivo definidos.
- Indicar si se requiere reproceso o cambio de regla.
- Mantener trazabilidad al flujo/tabla afectada.
