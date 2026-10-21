# Investigación — Auditoría (IA-B)

Aquí la IA-B registra el veredicto de cada hipótesis tras las pruebas de los pasos 4 a 7 del prompt maestro: APROBADA PARA PAPEL, CONDICIONAL o RECHAZADA, con la métrica que la descartó cuando aplique. La IA-B no reescribe hipótesis: las aprueba, las condiciona o las rechaza con justificación.

Los desacuerdos con la IA-A se escriben aquí con los argumentos de la IA-B, para que los decida Jane.

## Auditorías

### Lote 1 — auditoría del 2026-10-20

Universo congelado el 2026-10-20 ✔ · Aprobación de la dueña: recibida el 2026-10-20 · Contador global: 0 → **58**.

#### H-001 — Eventos USD de alto impacto (EURUSD, 5 min, MT5/AMP)

- **Paso 3 (formato): completo ✔.** Activo y fuente dentro del universo congelado (EURUSD vía AMP/MT5; temporalidad 5m ✔; el calendario económico es capa de datos del universo ✔).
- **Paso 1 (datos): NO superado hoy.** Los datos EURUSD 5m de la fuente congelada salen de la terminal MT5/AMP de la PC de la dueña y el puente de acceso está bloqueado; tampoco existe aún un calendario de eventos USD de alto impacto validado (preparación del Paso 1). Sustituir la fuente por otra violaría el universo congelado.
- **Pasos 4–7: no ejecutados** (sin datos no hay prueba). Pruebas sumadas al contador: **0**.
- **Veredicto: CONDICIONAL** — pendiente de datos. No es un rechazo de la idea: nunca fue probada. Se audita en cuanto los datos pasen el Paso 1.

#### H-002 — Ruptura de máximo de 20 días (BTC-USDT y ETH-USDT, OKX spot, diario)

- **Paso 3 (formato): completo ✔.** Activos dentro del universo (OKX ✔), temporalidad 1d ✔. Interpretaciones de mecánica de la IA-B (sin tocar la regla): stop fijo fijado al entrar (gestión: ninguna); cada operación se asigna al tramo de su fecha de entrada; las señales usan el calentamiento previo al tramo; cada señal opera (la regla no limita posiciones simultáneas).
- **Paso 1 (datos): superado ✔.** OKX diario, 2017-10-10 → 2026-10-19, 3.297 velas por activo. QC: 0 duplicados, 0 huecos, 0 OHLC incoherentes; en ETH, 2 saltos >30 % explicados (caídas de mercado del 2018-01-17 y del 2021-05-23). Partición: descubrimiento hasta 2023-03-10 · validación 2023-03-11 → 2024-12-28 · fuera de muestra desde 2024-12-29 (sellado). Costos aplicados: 0,05 % comisión + 0,02 % deslizamiento por lado.
- **Paso 4 (descubrimiento): superado por ambos.** BTC-USDT: 139 ops, PF 2,88, esperanza +9,68 %/op, acierto 56,8 %. ETH-USDT: 143 ops, PF 1,76, esperanza +5,43 %/op, acierto 54,5 %. (Umbral: PF > 1,05 y ≥ 30 ops.)
- **Paso 5 (validación): superado por ambos.** BTC-USDT: 52 ops, PF 3,06. ETH-USDT: 50 ops, PF 2,11. (Umbral: PF ≥ 1,15 y ≥ 20 ops.) Sensibilidad ±20 % (26 combinaciones nuevas por activo): 100 % con PF ≥ 1,0 en ambos. Estabilidad: BTC 4/4 bloques positivos, ETH 3/4. Costos al doble: BTC PF 2,98 · ETH PF 2,06 (> 1,0 ✔). Regímenes: no evaluable — no hay etiquetas de régimen disponibles.
- **Paso 6 (corrección por pruebas múltiples, Bonferroni con contador global = 58):** BTC-USDT: p sin ajustar 0,0000019 → ajustada **0,00011 ✔**. ETH-USDT: p sin ajustar 0,00087 → ajustada **0,0502 ✘** (el umbral es < 0,05). ETH-USDT no sobrevive la corrección — se queda a 0,0002 del umbral. La hipótesis, tal como está escrita (los dos activos), **no supera el Paso 6**.
- **Paso 7: NO ABIERTO.** El tramo fuera de muestra permanece sellado para ambos activos: no se consume por una hipótesis que no superó el Paso 6.
- Pruebas sumadas al contador: **58** (29 por activo: 1 descubrimiento + 1 validación + 26 de sensibilidad + 1 de costos dobles).
- **Veredicto: RECHAZADA (Paso 6).** Nota de la IA-B: BTC-USDT superó en solitario todos los pasos evaluables (4, 5 y 6). Si la IA-A lo desea, puede presentar una hipótesis NUEVA solo con BTC-USDT (id nuevo; contará como búsqueda nueva) y esa sí podría abrir el fuera de muestra.

#### H-003 — Reversión a la media entre pares (z-score, diario)

- **Paso 3 (formato): INCOMPLETO ✘.** El campo de activos dice "pares dentro de la misma fuente, a definir": no nombra ningún par. La IA-B no puede elegir el par sin reescribir la hipótesis, y eso el protocolo lo prohíbe.
- **Pasos 1 y 4–7: no ejecutados.** Pruebas sumadas al contador: **0**.
- **Veredicto: DEVUELTA A LA IA-A SIN PROBAR (Paso 3).** Para completarla: nombrar el par exacto (dos activos del universo congelado, de la misma fuente). Al volver completa se audita con el mismo id.

### Auditoría de H-004 — 2026-10-20

Aprobación de la dueña: recibida el 2026-10-20 · Contador global: 58 → **88**.

#### H-004 — Ruptura de máximo de 20 días, solo BTC-USDT (OKX spot, diario)

- **Paso 3 (formato): completo ✔.** Activo nombrado con exactitud (BTC-USDT, OKX spot — dentro del universo congelado ✔), temporalidad 1d ✔, todos los campos de la regla presentes. Es la hipótesis nueva solo-BTC que la auditoría de H-002 dejó abierta. Mismas interpretaciones de mecánica que en H-002 (sin tocar la regla): stop fijo fijado al entrar; operación asignada al tramo de su fecha de entrada; señales con calentamiento previo al tramo; cada señal opera.
- **Paso 1 (datos): superado ✔.** Mismo dataset validado en la auditoría de H-002: OKX diario, 2017-10-10 → 2026-10-19, 3.297 velas, QC limpio (0 duplicados, 0 huecos, 0 OHLC incoherentes). Misma partición congelada: descubrimiento hasta 2023-03-10 · validación 2023-03-11 → 2024-12-28 · fuera de muestra desde 2024-12-29. Costos aplicados: 0,05 % comisión + 0,02 % deslizamiento por lado.
- **Paso 4 (descubrimiento): superado ✔.** 139 ops, PF 2,88, esperanza +9,68 %/op, acierto 56,8 %. (Umbral: PF > 1,05 y ≥ 30 ops.) Son los mismos números de la pata BTC-USDT de H-002: misma regla y mismos datos.
- **Paso 5 (validación): superado ✔.** 52 ops, PF 3,06, esperanza +5,50 %/op, acierto 69,2 %. (Umbral: PF ≥ 1,15 y ≥ 20 ops.) Sensibilidad ±20 % (26 combinaciones nuevas): 100 % con PF ≥ 1,0. Estabilidad: 4/4 bloques positivos. Costos al doble: PF 2,98 (> 1,0 ✔). Regímenes: no evaluable — no hay etiquetas de régimen disponibles, igual que en H-002.
- **Paso 6 (corrección por pruebas múltiples, Bonferroni con contador global = 87 al momento del ajuste):** p sin ajustar 0,0000019 → ajustada **0,00017 ✔** (umbral < 0,05). Superado.
- **Paso 7 (fuera de muestra, ABIERTO para esta hipótesis): NO superado ✘.** Tramo sellado 2024-12-29 → 2026-10-19, corrido una sola vez: **35 operaciones, PF 0,86, esperanza −0,47 %/op, acierto 40,0 %, resultado acumulado −16,44 %**. Criterios del Paso 7: ≥ 30 ops ✔ (35) · PF ≥ 1,10 ✘ (0,86) · esperanza positiva ✘ (−0,47 %) · último trimestre positivo ✔ (8 ops con entrada desde 2026-07-01, neto +8,60 %). Detalle: 18 entradas en 2025 y 17 en 2026; 14 ganadoras de 35; peor operación −11,29 % (entrada 2025-10-03); mejor operación +14,94 % (entrada 2026-08-19).
- Pruebas sumadas al contador: **30** (1 descubrimiento + 1 validación + 26 de sensibilidad + 1 de costos dobles + 1 de fuera de muestra). **Contador global: 88.**
- **Veredicto: RECHAZADA (Paso 7).** La regla ganó en descubrimiento y en validación (2017–2024) y perdió en el tramo que nadie había mirado (2025–2026): el fuera de muestra hizo el trabajo para el que estaba sellado. Que el último trimestre salga positivo no la salva — los criterios del Paso 7 se cumplen todos o la hipótesis no pasa. No va a papel. La IA-B no propone variantes: cualquier cambio de parámetros, de activo o de temporalidad es una hipótesis nueva de la IA-A, con id nuevo, y sumará al contador.
