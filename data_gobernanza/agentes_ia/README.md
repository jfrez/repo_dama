# Agentes IA de apoyo (demo educacional)

Ejemplos de roles que se pueden cargar en `codex-cli` (ver `agents.md` en la raíz de `educacional/`):

- **Curador de diccionario**: revisa `data_gobernanza/diccionarios/tablas.md` y sugiere mejoras de definiciones o campos faltantes.
- **Vigilante DQ**: lee `data_gobernanza/dq_reglas/reglas.md` y `tmp/dq_resumen.csv` para proponer acciones correctivas.
- **Documentador de flujos**: sintetiza qué hace cada script en `data_01*`/`data_02*` y genera un registro de decisión o minuta.

Prompts de ejemplo:
- "Usa el diccionario y las reglas DQ para preparar una ficha de datos de `dm_sales_diarias` en tono ejecutivo."
- "A partir de `tmp/dq_resumen.csv`, arma un mini informe con hallazgos y próximas acciones."
- "Resume en 10 líneas el linaje de `core_ordenes` indicando qué columnas se calculan y de dónde provienen."
