---
tags: [trading]
---
# Bitunix XRPUSDT — auditoría de la estrategia micro-scalping (2026-10-04)

Tema: [[Trading]] · [[Bitunix]]

## Veredicto
**La idea EMA 9/21 + RSI + volumen NO tiene ventaja. DO NOT DEPLOY.**
La única señal que sobrevive es una **reversión a la media muy selectiva**: **PAPER ONLY**, con ganancia real de centavos al día. **$20/día con $35 es matemáticamente imposible.**

## Datos usados
- 387,559 velas de 1 minuto de XRPUSDT (Bitunix), 2026-01-07 a 2026-10-04 (270 días).
- Partición por tiempo: **entrenamiento** hasta 22-may, **validación** hasta 29-jul, **OOS** hasta 4-oct.
- **No existe order-book histórico**: solo la foto del momento. Hipótesis conservadora: spread + slippage en ticks (1 tick = 0.0073%).
- Motor: señales con barras cerradas, entrada en la apertura del 1m siguiente, SL antes que TP en la misma vela, funding 0.015%/8h. Validado con entradas aleatorias (da justo el costo).

## Comisiones reales (verificado con tus posiciones cerradas)
- 8 de 10 cierres de XRP: **fee = 0** (SL, TP y mercado).
- Las 2 con fee (0.0253%) fueron **liquidaciones** del 2-oct a 100x.
- Con 2x aislado no hay riesgo de liquidación. Costos que quedan: spread, slippage y funding.

## Hallazgo grave: el paper estaba inflado
`lab.py` resuelve el TP/SL con la **vela que acaba de cerrar** (la misma que generó la señal). **136 de 199 operaciones del paper se resolvieron en menos de 30 s** (imposible): 74% de aciertos y +$465 de los +$506 totales. Las 63 restantes: **49% de aciertos**. Los resultados del paper no son confiables.

## Resultados (después de costos "base")
| Familia | Configs | Mejor expectancy OOS media | % configs rentables en OOS |
|---|---|---|---|
| EMA 9/21 + RSI + volumen | 4,032 | **−0.026%** por operación | 1% |
| Momentum (ruptura + volumen) | 1,344 | −0.0215% | 4% |
| Reversión a la media | 1,960 | −0.0045% | 39% |
| **Bot actual (BB_RSI 5m, 1.5σ, RSI 35/65)** | — | **−0.0008%** (PF 0.99), −0.014% con costo conservador | — |

## Candidato C1 (el único que sobrevive)
5 min · Bollinger(14, 2.5σ) · RSI ≤25 largo / ≥75 corto · TP 0.3% / SL 0.2% · 1 posición.
- 305 operaciones (**1.13/día**), win **47.5%**, **PF 1.29**, expectancy **+0.0313%** (+0.157R) por operación.
- Ganador medio +0.294%, perdedor medio −0.206%. Duración media 10 min. MAE 0.21%, MFE 0.24%.
- OOS: PF 1.39, +0.041%. Costo conservador: PF 1.16, +0.0185%.
- Bootstrap IC95% [+0.003, +0.060]%.
- Estable por vecinos: más extremo (2.5σ, RSI≤25) = mejor, con patrón monótono; todos los TP/SL cercanos positivos.
- **Menos operaciones = mejor**: 1.5σ/RSI35 (30 señales/día) ≈ 0; 2.5σ/RSI25 (1/día) +0.031%.
- 8 de 10 meses positivos. Peor: mayo.
- Largos y cortos similares. Mejores horas UTC: **08–12**.
- **Volatilidad baja pierde** (−0.05%). Filtro calibrado solo con entrenamiento: n=205, +0.070%, PF 1.76, positivo en validación y OOS.
- BE y trailing: no mejoran (tabla: BE baja el acierto; trailing ≈ igual).
- Con $35, 2x: **$35 → $42.21 en 270 días** (+20.6%), DD máx 6.5%, Sharpe 2.5, racha perdedora máx 9 (p95: 6).
- Monte Carlo ($35, 2x, kill −$1/día): 90 días mediana $37.2, p5 $34.2, P(perder >25%) 0%, P(<$10) 0%.

**Advertencia:** C1 es el mejor de ~1,850 configuraciones; con 305 operaciones puede haber sobreajuste. Sirve para paper, no para real.

## Objetivo diario
| $/día | Retorno diario necesario sobre $35 | Capital necesario a 2x | A 10x |
|---|---|---|---|
| 1 | 2.9% | $1,412 | $282 |
| 2 | 5.7% | $2,824 | $565 |
| 5 | 14.3% | $7,060 | $1,412 |
| 10 | 28.6% | $14,119 | $2,824 |
| 20 | 57.1% | $28,238 | $5,648 |

La estrategia produce **~$0.03/día** con $35. Para $20/día con $35 a 2x hace falta ~25% neto por operación (medido: 0.03%).

## Kill switch propuesto (si algún día va a real)
- Pérdida máxima diaria: −$1 (≈3%).
- Parar tras 5 pérdidas seguidas (p95 histórico = 6).
- Detener al bajar 15% desde el máximo ($29.75).
- Máx. 3 operaciones/día, 1 posición, 2x aislado, sin martingala.
- Datos con más de 90 s sin actualizar → no operar. Bloquear volatilidad baja.

## Siguientes pasos (pendientes de autorización)
1. Arreglar el paper (resolver solo con velas posteriores a la entrada).
2. Correr C1 en demo 4–8 semanas y comparar con el backtest.
3. Solo si coincide, preparar versión real con los controles.

Scripts: `Bitunix Proyecto/auditoria/`.
