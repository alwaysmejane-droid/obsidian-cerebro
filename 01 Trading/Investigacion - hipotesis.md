# Investigación — Hipótesis (IA-A)

Aquí la IA-A escribe sus hipótesis ANTES de correr cualquier prueba, con el formato del prompt maestro: id, fecha, tipo, razón, reglas exactas (entrada, dirección, stop, objetivo, salida por tiempo, gestión, tamaño), activos y timeframe dentro del universo congelado, y parámetros fijos.

La IA-B no edita esta nota: la lee y responde en la nota de auditoría.

## Hipótesis

## Lote 1 (borrador)

### H-001

- **fecha:** 2026-10-20
- **tipo:** horario y calendario
- **razón:** Los eventos de alto impacto de USD (datos de empleo, inflación, decisiones de tasas) generan desequilibrio de órdenes en los minutos siguientes; el precio tiende a reaccionar de forma sostenida cuando el primer movimiento tiene cuerpo fuerte. Mecanismo: flujo de órdenes y reajuste de posiciones.
- **entrada:** cierre de la primera vela de 5 min posterior a la hora del evento; solo si su cuerpo es mayor al 60 % del rango.
- **dirección:** largo si la vela cierra alcista; corto si cierra bajista.
- **stop:** 1,0 × ATR(14) de velas de 5 min, medido desde la entrada.
- **objetivo:** 2R (2 veces el stop).
- **salida por tiempo:** 12 velas de 5 min.
- **gestión:** ninguna.
- **tamaño:** 5 USD de riesgo por operación.
- **activos:** pendiente de universo (candidato de la familia: EURUSD por MT5/AMP).
- **timeframe:** 5 min.
- **parámetros:** ATR 14; cuerpo mínimo 60 %; objetivo 2R; tiempo 12 velas.

### H-002

- **fecha:** 2026-10-20
- **tipo:** estructura de precio
- **razón:** Las rupturas de máximos de largo plazo atraen órdenes de compra de seguidores de tendencia y de cierres de cortos, lo que puede sostener el movimiento varios días. Mecanismo: liquidez en niveles conocidos.
- **entrada:** cierre de la vela diaria que supera el máximo de los últimos 20 días.
- **dirección:** solo largo.
- **stop:** mínimo de los últimos 10 días.
- **objetivo:** ninguno.
- **salida por tiempo:** 20 velas diarias.
- **gestión:** ninguna.
- **tamaño:** 1 % del capital de la cuenta.
- **activos:** pendiente de universo (candidato de la familia: BTC-USDT y ETH-USDT en OKX).
- **timeframe:** 1 día.
- **parámetros:** máximo de 20 días; mínimo de 10 días; tiempo 20 velas.

### H-003

- **fecha:** 2026-10-20
- **tipo:** matemática (relación entre activos)
- **razón:** Dos activos de la misma familia tienden a volver a su relación media después de separarse. Mecanismo: arbitraje entre contratos relacionados y reequilibrio de carteras.
- **entrada:** cuando el z-score de la relación de precios de 30 días llega a menos -2 (compra la relación) o más 2 (vende la relación); evaluado al cierre diario.
- **dirección:** ambos, con una pata por activo.
- **stop:** z-score de 3 en contra de la entrada.
- **objetivo:** z-score de 0 (media).
- **salida por tiempo:** 30 velas diarias.
- **gestión:** ninguna.
- **tamaño:** 1 % del capital, repartido en las dos patas.
- **activos:** pendiente de universo (candidato de la familia: pares dentro de la misma fuente, a definir).
- **timeframe:** 1 día.
- **parámetros:** ventana 30 días; entrada ±2; stop 3; tiempo 30 velas.

### H-004

- **fecha:** 2026-10-20
- **tipo:** estructura de precio
- **razón:** la misma de H-002: las rupturas de máximo de largo plazo atraen compras de seguidores de tendencia y cierres de cortos. Mecanismo: liquidez en niveles conocidos. Nota: BTC-USDT ya apareció en la auditoría de H-002; el tramo fuera de muestra es la única prueba limpia.
- **entrada:** cierre de la vela diaria que supera el máximo de los últimos 20 días.
- **dirección:** solo largo.
- **stop:** mínimo de los últimos 10 días.
- **objetivo:** ninguno.
- **salida por tiempo:** 20 velas diarias.
- **gestión:** ninguna.
- **tamaño:** 1 % del capital.
- **activos:** BTC-USDT (OKX spot).
- **timeframe:** 1 día.
- **parámetros:** máximo 20 días; mínimo 10 días; tiempo 20 velas.
