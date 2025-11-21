# Ejemplo de gobierno y politicas

| Dominio | Data Owner | Steward | Ingenieria | Clasificacion | Criterio de acceso | Excepciones |
| --- | --- | --- | --- | --- | --- | --- |
| Ventas ecommerce | Equipo docente | Tutor de datos | Equipo tecnico | Interno | Solo usuarios del curso con rol lector; cambios por PR revisado por steward | Acceso temporal a invitado (15 dias) para debug de taller #3, aprobado 2024-05-02 |

- Retencion: datos raw 90 dias, stage/core/dm 180 dias; reportes en `tmp/` se purgan semanalmente.
- Revision de SLA: mensual; desvio se documenta en `operacion_continuidad/ejemplo_runbook.md`.
