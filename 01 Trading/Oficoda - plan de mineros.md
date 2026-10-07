---
tags: [trading]
---
# La Oficoda — plan de mineros de estrategias (2026-10-07)

Tema: [[Trading]] · Proyecto: [[Bitunix]]

## Idea
Agentes con distintas formas de operar buscan estrategias en cripto de Bitunix. Todas pasan por el mismo embudo de pruebas y se miden igual. Lo real solo con autorización explícita; antes, paper 4–8 semanas.

## Universo (2026-10-07)
**Nivel 1: lista "0 Fees" de Bitunix** (captura del 2026-10-07): SOLUSDT, XRPUSDT, DOGEUSDT, CLUSDT, BZUSDT, XAGUSDT, XAUUSDT.
- Ojo: la promo de 0 comisiones puede acabar. Toda estrategia se prueba **con comisión cero y con comisión normal**.
- Metales y petróleo (XAU, XAG, CL, BZ): sin datos de operaciones (ticks) gratis, solo velas.

**Nivel 2: líquidas para vigilar** (volumen 24h > ~$15M): BTC, ETH, ZEC, NEAR, SUI, BNB, HYPE, ADA, AVAX, LINK, TAO, UNI.
- Hay ~800 mercados; la mayoría son poco líquidos y el deslizamiento se come cualquier ventaja. Se descartan.

## Mineros (estilos)
1. ICT (barridos de liquidez, FVG, zonas de oferta/demanda, horas de sesión)
2. SMC (BOS/CHoCH, order blocks)
3. Order flow (delta, absorción, perfil de volumen)
4. Tendencia / momentum
5. Reversión a la media / volatilidad

Cada idea debe quedar escrita como **reglas exactas** (sin interpretación) para poder probarla.

## Embudo (igual para todos)
Propuesta → programar → backtest (comisiones y deslizamiento reales, sin mirar el futuro) → datos que nunca vio (OOS) y walk-forward → debe funcionar en **varias monedas** → corrección por probar muchas ideas → intento de romperla → paper 4–8 semanas → decisión real solo con OK explícito.

## Organización por departamentos (decisión 2026-10-07)
Meta final: lo que sobreviva alimenta el bot de **Bitunix Lab** (paper realista) y luego el real, solo con OK explícito. Idea: 1–3 estrategias por modalidad (swing, day, scalping).
1. **Traders, en parejas** (ninguno tiene la última palabra; la idea sale solo si los dos están de acuerdo y se guarda el desacuerdo): pareja Swing, pareja Day trading, pareja Scalping, con estilos distintos (ICT, SMC, order flow, tendencia, reversión).
2. **Backtesting** (2 personas): programan y prueban con reglas fijas.
3. **Destrucción** (2 personas): intentan romper cada estrategia.
4. **Bitunix Lab** (paper realista, 4–8 semanas).
5. **El bot.** Real solo con autorización de la jefa.
Compuertas: pareja de acuerdo → backtest pasa → destrucción no la rompe → paper realista → OK de la jefa.

## Ideas tomadas de otro bot (ejemplo, captura 2026-10-07)
Un bot de terceros ("Búho Bot") muestra ideas útiles. Sus cifras (64%, 71%) son suyas y no verificadas; solo copiamos el concepto.
- **Filtro por sesión** (Asia, Londres, NY mañana, NY tarde, noche) con la tasa de acierto medida de cada una → nosotros la medimos con datos propios.
- **Reglas de riesgo diario:** máximo de operaciones al día, parar tras ganar una, parar tras 2 pérdidas seguidas, no operar antes/después de noticias fuertes (CPI, FOMC), fines de semana aparte.
- **Estrategia ejemplo:** barrida de liquidez + agotamiento, con TP en el POC → candidata para los mineros ICT y order flow.
- **Panel de control:** encendido/apagado, resultado de hoy y de la semana, operación abierta.

## Pendiente
- [ ] Corregir el error del paper en `bitunix-lab` (mira la vela de la señal). Falta autorización.
- [ ] Bajar datos de velas 1m de Nivel 1 y 2.
- [ ] Datos de operaciones (delta) de Binance para las monedas que existan allá.
- [ ] Motor de pruebas común (reusar `Bitunix Proyecto/auditoria`).
- [ ] Dar vida a los mineros en [[La Oficoda]] (panel en el puerto 8797).
