# Reglas DQ en ingesta (raw)

Registra los controles aplicados al recibir los datos.

Incluye:
- Campos obligatorios, tipos esperados y validaciones de rango basicas.
- Duplicados en claves naturales y como se manejan (rechazo, marca, consolidacion).
- Clasificacion de errores y donde se dejan evidencias (logs en `tmp/`, alertas).
- Responsables y ventanas de lookback usadas en ingestas progresivas.

Relaciona estos controles con las fuentes descritas en `../../metadata/fuentes/`.
