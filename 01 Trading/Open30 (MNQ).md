---
tags: [trading]
---
# Open30 (MNQ)

Tema: [[Trading]]

Única estrategia de MNQ. Reemplazó a thewhale y open15.

## Reglas
- Caja 9:00–9:30 NY (velas de 5m). Cierre ≥30 pts fuera de la caja → entrada en la apertura de la vela siguiente.
- Rompe arriba = compra; rompe abajo = venta (continuación).
- SL 70% / TP 100% de la distancia de la caja (RR 1:1.43). 5 contratos, tope $700 de riesgo.
- Sin escalera (añadir contratos fue dañino en 5 años). Cierre forzado 15:00. Una operación por día. Solo NY.

## Estado
- Backtest limpio sin filtros: +$54,363.60 (SL 70%).
- Corre en vivo en el servicio `open30`; copiador a 6 cuentas en el dashboard.
- Indicadores: TradingView y MT5 (`MNQ proyecto`).

Ver [[Propfirms]].