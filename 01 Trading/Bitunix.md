---
tags: [trading]
---
# Bitunix

Tema: [[Trading]]

## Real (desde 2026-10-04)
- Solo **XRPUSDT**. Riesgo **$2 por operación** (pérdida máxima). Apalancamiento **10x**. **Máximo 2 posiciones abiertas** a la vez; si ya hay 2, la señal se descarta. BE a +$1 (SL a la entrada +0.02%). Cuenta ~$38. Configurado 2026-10-15 en `bitunix_live.py` (RISK_USD, LEVERAGE, MAX_OPEN); **sin activar**.
- **Plan real confirmado 2026-10-15** (sin activar; el bot real aún no programa estas estrategias):
  - Bollinger ruptura + volumen 15m: principal **SKHYNIXUSDT**, respaldo **ZECUSDT**.
  - Pullback ema 1h: principal **SKHYNIXUSDT**, respaldo **SPCXUSDT**.
  - Cada estrategia: máximo 1 posición abierta, $2 de pérdida máxima, **15x** (con 10x dos posiciones no caben en ~$38). Global: máximo 2 posiciones.
  - Verificado en la API pública: SKHYNIX, ZEC y SPCX están OPEN y con API. Mínimos: SKHYNIX 0.01, ZEC 0.006, SPCX 0.05. Apalancamiento máximo: SKHYNIX 50x, ZEC 75x, SPCX 50x.
  - Muestra pequeña en paper (4–7 operaciones por activo): revisar con más datos.
- **Programado 2026-10-15** en `Bitunix Proyecto/bitunix_real.py` (sin activar, probado solo con velas públicas): BOLL_VOL_15M y PULLBACK_EMA_1H, una posición por estrategia, respaldo si el principal no entra. `bitunix_live.py` ahora guarda la estrategia en cada orden. Supuesto: ATR de 14 (el ruedo no guarda la longitud).
- Pendiente antes de activar: trailing (hoy solo hay BE), verificar mínimo de XRP que no supere $2 de pérdida, y que `BITUNIX_LIVE_TRADING=1` lo ponga la dueña en `.env`.
- Parar: crear archivo `LIVE_STOP` en `Bitunix Proyecto` (ya existe: el bot está apagado).
- CLUSDT quedó en paper: su SL muy corto pide ~$65 de margen. Se reactiva con ~$70 libres.

## Lo que aprendí
- El paper se ve mejor que el real: slippage 10–14% y rechazos (error 30032, TP ya superado) cuando el precio se mueve.
- Ventaja no probada: muestra pequeña (días).
- Estrategia: BB_RSI.