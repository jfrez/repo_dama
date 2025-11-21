# Gobernanza de datos (demo educacional)

Este directorio muestra cómo documentar y controlar el linaje de datos del proyecto educativo:

- **Diccionarios** (`diccionarios/`): definiciones de tablas y campos de las capas raw, stage, core y dm.
- **DQ** (`dq_reglas/`): reglas de calidad aplicadas en la ingesta y en la consolidación, con responsables y umbrales.
- **Metadata** (`metadata/`): información de catálogo, fuentes y periodicidad.
- **Agentes IA** (`agentes_ia/`): prompts de apoyo para mantener la documentación y revisar cumplimiento.

Cada vez que se cambie un proceso en `data_0X_*`, actualiza la documentación correspondiente y registra supuestos o decisiones.
