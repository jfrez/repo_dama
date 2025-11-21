# Dominio: Ventas (continuo)

- **Objetivo**: traer órdenes nuevas/actualizadas, pagos e inventario vía API (o fixture) y cargar solo los registros recientes.
- **Script/flujo**: `api/carga_progresiva.py` (`edu_api_progressive_flow`).
- **Entrada**: API real (`EDU_API_URL`) o fixture `api/fixtures/ventas_incremental.json`.
- **Ventana incremental**: `EDU_PROGRESSIVE_LOOKBACK_DAYS` (default 7 días) aplicada sobre `updated_at`.
- **Salida**: inserta en `raw_ordenes_api`, `raw_order_items_api`, `raw_payments_api`, `raw_inventory_api` y registra en `control_ejecuciones`.

Ejecución rápida:
```bash
python educacional/data_01_adquisicion/continuo/ventas/api/carga_progresiva.py
```
Usa `EDU_API_MODE=online` y `EDU_API_URL` para probar contra un endpoint real.
