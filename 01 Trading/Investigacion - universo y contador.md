# Investigación — Universo y contador (IA-B)

**UNIVERSO CONGELADO — 2026-10-20** (fijado por la IA-B bajo las reglas de la dueña).
Este documento no se reescribe tras el congelamiento. Los activos que la dueña pida después entran por **adenda fechada** al final de esta nota, y cada adición suma al contador como búsqueda nueva.

## Regla de inclusión (de la dueña, 2026-10-20)

Ningún activo, fuente ni temporalidad se descarta de entrada. Bitunix, OKX, Binance, AMP/MT5, futuros, cripto, forex o cualquier otro entran al universo si la dueña los pide. El universo cubre varias fuentes y familias de mercado; nadie se casa con una sola fuente ni con un solo activo.
Cada activo o temporalidad que se agregue cuenta como búsqueda nueva para la corrección por pruebas múltiples y se registra en el contador — eso no es razón para excluirlo.

## Fuentes y activos del universo (v1)

**Bitunix — futuros USDT:**
BTCUSDT, ETHUSDT, SOLUSDT, XRPUSDT, DOGEUSDT, XAUUSDT (oro), XAGUSDT (plata), CRCLUSDT (petróleo WTI), Brent, SAMSUNGUSDT, SKHYNIXUSDT, SKHYUSDT, SNXXUSDT, KORUUSDT. Velas, volumen, funding; open interest si la API lo entrega.

**OKX — spot y futuros (swaps):**
BTC, ETH, SOL, XRP, DOGE (pares USDT y swaps perpetuos). Velas diarias y horarias; open interest histórico diario.

**Binance — futuros USDⓈ-M:**
BTCUSDT, ETHUSDT, SOLUSDT, XRPUSDT, DOGEUSDT (perpetuos). Velas, volumen, funding, open interest.

**AMP / MetaTrader 5 (demo) — futuros CME y forex:**
NQ, MNQ, ES, MES, GC (oro), CL; EURUSD, GBPUSD, USDJPY, y cualquier otro símbolo disponible en la terminal. Velas M1 a D1.
_Nota de la IA-B: la extracción de datos de AMP/MT5 depende hoy del acceso a la PC de la dueña (puente actualmente bloqueado). Es una dependencia de datos del Paso 1, **no** una exclusión del universo: los activos quedan dentro y sus hipótesis esperan a que los datos pasen los controles de calidad._

**Calendario económico (capa de datos, no es un activo):**
eventos de alto impacto de USD (fecha, hora, tipo).

**Agentes de OmniRoute (capa de clasificación, nunca fuente de señal):**
clasificaciones con reglas fijas, p. ej. régimen de mercado del día.

## Temporalidades

Todas las disponibles por fuente: 1m, 5m, 15m, 1h, 4h, 1d. Ninguna se descarta de entrada; cada combinación activo × temporalidad que se pruebe suma al contador.

## Partición (congelada)

Cronológica, por activo, sobre su cobertura validada en el Paso 1:
- **Descubrimiento: 60 %** (el tramo más antiguo)
- **Validación: 20 %**
- **Fuera de muestra: 20 %** (el más reciente — **sellado: nadie lo mira hasta el Paso 7**)

Las fechas exactas de corte de cada activo se registran en sus metadatos al validar sus datos (Paso 1); registrarlas no modifica el universo.

## Contador de pruebas

- Regla: +1 cada vez que se prueba una regla, un parámetro, un activo o una temporalidad (incluye cada hipótesis, cada variante de sensibilidad y cada adenda de activo).
- **Pruebas acumuladas al congelar: 0**
- **Pruebas acumuladas tras el lote 1 (2026-10-20): 58**

Registro del contador:
- 2026-10-20 — Lote 1, H-002: 58 pruebas (BTC-USDT 29 + ETH-USDT 29: descubrimiento, validación, 26 combinaciones de sensibilidad y costos dobles, por activo). H-001: 0 (condicional, sin datos). H-003: 0 (devuelta en el Paso 3). **Total global: 58.**

## Adendas

_(Ninguna todavía. Cada adenda llevará fecha, activo/fuente/temporalidad agregados y el motivo: pedido de la dueña.)_
