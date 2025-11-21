# Esquema de gestion y gobernanza de datos (DAMA)

Guia breve para ordenar procesos, etapas y tareas del demo educacional siguiendo los dominios de DAMA-DMBOK y manteniendo evidencias en `data_gobernanza/`.

## Principios adaptados
- Gobierno y politicas: roles claros (Data Owner, Steward, Eng), criterios de acceso y excepciones registradas.
- Arquitectura y modelado: capas raw/stage/core/dm, convenciones de nombres y claves de negocio/versionado.
- Metadata y catalogo: fuente, periodicidad, contacto, SLA, criticidad, ubicacion y linaje documentados.
- Calidad de datos: reglas preventivas y detective, umbrales, responsables y bitacora de brechas.
- Seguridad y privacidad: clasificacion de datos, mascaras en datasets sensibles, control de uso y retencion.
- Operacion y continuidad: agendas de ejecucion, observabilidad, planes de recuperacion/reprocesos.

## Etapas y tareas recomendadas
### 01. Adquisicion (raw) — `data_01_adquisicion/*`
- Proposito: ingresar datos tal como llegan, preservando contrato original y trazabilidad.
- Tareas clave: definir contrato de fuente (campos, tipos, horario, SLA), registrar metadata y clasificacion, crear diccionario raw, definir reglas DQ minimas (obligatorios, tipos, duplicados basicos), probar cargas piloto.
- Operacion: scripts de historico `historico/*/carga_inicial.py` y continuo `continuo/ventas/api/carga_progresiva.py`. Log de ejecucion y evidencias de DQ en `tmp/`.

### 02. Integracion (stage/core/dm) — `data_02_integracion/*`
- Proposito: normalizar y consolidar dominios con claves maestras y reglas comunes.
- Tareas clave: mapear campos raw->stage, estandarizar codigos/temporalidad, asegurar granularidad consistente, definir reglas DQ de negocio (unicidad, referencial, balances), actualizar diccionarios stage/core/dm y linaje.
- Operacion: `01_construccion/stage_comercio.py` (stage), `02_procesamiento/revision_calidad.py` (DQ resumen en `tmp/dq_resumen.csv`), `03_consolidacion/consolidar_modelo.py` (core y datamarts).

### 03. Operacion y observabilidad — `data_03_operacion/*`
- Proposito: verificar salud de cargas y productos.
- Tareas clave: capturar metricas de ejecucion (tiempos, filas, fallos), revisar alertas de DQ, validar SLA, mantener plan de reprocesos.
- Operacion: `monitoreo/resumen_ejecuciones.py` genera `tmp/monitoreo_resumen.csv` con control de ejecuciones y salidas clave.

### 04. Usos y productos — `data_04_usos/*`
- Proposito: exponer productos confiables y versionados.
- Tareas clave: definir owner y consumidor, SLA de disponibilidad/frescura, contratos de salida (layout, definiciones), controles de acceso y retencion, feedback a ingeniería cuando haya brechas.
- Operacion: `reportes/reporte_resumen.py` produce consumos simples (`tmp/reporte_ventas.csv`, `tmp/reporte_pagos.csv`).

## Artefactos obligatorios en `data_gobernanza/`
- `diccionarios/`: definiciones por capa (campo, tipo, calculo/transformacion, sensibilidad, owner).
- `dq_reglas/`: reglas con dominio, punto de control (ingesta/integracion/consumo), umbral, responsable y accion ante brecha.
- `metadata/`: fichas de fuente/producto (periodicidad, medio de entrega, SLA, contacto, criticidad, retencion).
- `agentes_ia/`: prompts de apoyo para mantener la documentacion alineada con las politicas.

## Checklist por flujo (ejemplo)
- Planificar: contrato de datos firmado (fuente, SLA, formato), clasificacion y controles de acceso definidos.
- Diseñar: diccionario actualizado y mapeo raw->stage/core, reglas DQ asignadas y versionadas.
- Ejecutar: evidencia de corrida (timestamp, filas leidas/escritas) y logs de errores.
- Verificar: resumen DQ y monitoreo adjuntados en `tmp/`, brechas registradas con responsable y fecha de mitigacion.
- Documentar: actualizar `data_gobernanza/*` y linaje cada vez que cambie la frecuencia, la logica o la fuente.

## Ejemplos aplicados al demo
- Clientes/Catalogo/Ordenes historico: contrato CSV, diccionario raw, reglas de obligatoriedad y duplicados, carga con `carga_inicial.py`, registro de filas y timestamp.
- Ventas/Inventario continuo via API/fixture: definir lookback (`EDU_PROGRESSIVE_LOOKBACK_DAYS`), version de API usada, SLA de ingesta, alertas por faltantes; usar `carga_progresiva.py`.
- Calidad integrada: correr `revision_calidad.py` tras ingestas y antes de consolidar; guardar resumen en `tmp/` y anexar caso de brecha en `dq_reglas`.
- Consolidacion y consumo: `consolidar_modelo.py` publica core/dm; `reporte_resumen.py` expone CSV a analistas. Documentar producto, owner y requisitos de acceso.
