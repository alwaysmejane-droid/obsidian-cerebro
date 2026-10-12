# Estrategias rentables (candidatas que sobrevivieron la destrucción)
_Las anota la Oficoda automáticamente. Candidata no significa aprobada: falta demo/paper._

## 2026-10-07 22:06 · RSI extremo + solo compras · DIARIO · [[d80954995]]
- Activos: MES, MNQ, MYM, MGC · fuera de muestra 199 ops, 0.221 R/op, z=3.50
- Informe completo: Informes futuros/d80954995.md

## 2026-10-09 08:32 · London Session Breakout Strategy · FUTUROS
- Origen: Minería (código abierto) / 137195 (estudiante fut_bt)
- Activos: MES, MNQ, MYM, MGC · velas de 5 min
- Fuera de muestra: 852 ops, 0.269 R por operación, z=5.81, acierto 50%; validación 0.166 R; entrenamiento 0.289 R
- Destrucción: x2 +0.221R; retraso +0.259R; vecinos 6/6; z mínimo 4.80 tras 62672 pruebas
- Recomendaciones:
  - Operar solo en: MES, MNQ, MYM, MGC (los activos donde sobrevivió; no hay evidencia en el resto).
  - Marco de 5 minutos; parámetros: {"sl_atr": 2.115, "tp_atr": 6.288, "session_start": 995, "session_end": 369, "entry_end": 1271}.
  - Usar primero en demo con órdenes reales y revisar el deslizamiento medido frente al del backtest.
  - No usar dinero real ni cuentas de fondeo hasta que apruebe la demo y la simulación de evaluación de Zoila dé valor esperado positivo.
