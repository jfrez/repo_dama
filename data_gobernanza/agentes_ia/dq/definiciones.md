# Definiciones y severidades (DQ)

- Severidad alta: pérdida de PK, referencial rota, montos desbalanceados, datos personales sin mascarar.
- Severidad media: nulos en campos obligatorios de negocio, montos negativos, duplicados no esperados.
- Severidad baja: missing opcionales, warnings de lookback, campos sin catálogo.
- Acción: reproceso inmediato (alta), ajuste en siguiente ciclo (media), backlog/documentar (baja).
- Responsables: Data Engineer (pipeline), Data Steward (regla/catálogo), Data Owner (decisión de negocio).
