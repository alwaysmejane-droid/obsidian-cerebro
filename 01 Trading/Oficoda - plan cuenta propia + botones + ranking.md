# Plan: cuenta propia $200 (nanos), botones en Abiertas y ranking de estrategias
_Pedido de la dueña el 2026-10-13. NO construido: el límite semanal llegó al 100 %. Retomar tras el reinicio semanal (2026-10-13 22:00 UTC)._

## 1. Cuenta propia de $200 en futuros (nanos)
- Tercera cuenta de la arena, además de Bitunix ($200 virtuales por estrategia) y Futuros (cuentas 25k de fondeo simuladas).
- **Capital propio $200, sin reglas de fondeo** (sin tope de pérdida diaria, sin «cuenta quemada», libertad para abrir y cerrar rápido). Acepta ganar menos.
- Mismos activos y mismos datos (MT5/AMP) y mismas estrategias que la arena de Futuros (MES, MNQ, MYM, MGC), con **máximo 3 contratos nanos**.
- **DATO CONFIRMADO (2026-10-13, tabla de CME que mandó la dueña): E-nano** = 1/10 del micro. NES (S&P 500) $0.50/pt, NNQ (Nasdaq-100) $0.20/pt, N2K (Russell 2000) $0.50/pt, NDOW (Dow Jones) $0.05/pt. **No hay nano de oro** (MGC no aplica a esta cuenta). Mapa: MES→NES (0.5), MNQ→NNQ (0.2), MYM→NDOW (0.05). Ya no hace falta inventar el valor; se usan los mismos precios de MES/MNQ/MYM con ese valor por punto, máx 3 contratos.
- ~~Pendiente de investigar:~~ (resuelto arriba; texto anterior:) valor por punto de un «nano» (mucho menor que el micro: MES $5/pt, MNQ $2/pt, MYM $0.5/pt, MGC $10/pt). La dueña dice que lo busque yo; no existen nanos CME de índices que yo conozca, así que probablemente es una fracción del micro (p. ej. 0,1 micro). **Definir con ella el valor por punto simulado** y el broker que ella busque. Comisión: la que pondrá ella o la de siempre.
- Horario igual que Futuros: dom 18:00 a vie 15:15, plano a 15:30, pausa 15:30–18:00.
- Riesgo por operación debe caber en $200 (stop en dólares pequeño): definir % de riesgo (p. ej. 2–5 %).

## 2. Botones en la pestaña «Abiertas» (docks Bitunix y Futuros, en la oficina)
- Por posición: **Proteger** (stop a break-even + costos) y **Cerrar** (a mercado). También «cerrar todas».
- Aplica a posiciones **simuladas de la arena** (Bitunix y Futuros) y a la cuenta propia. Bitunix real NO está activado; no ejecutar nada real. La demo de AMP de Julián sigue en pausa (no tocar sus stops).
- Backend: endpoints POST en `Agentes/server.py` (patrón de `/api/accion`) que llamen a `arena.cerrar_pos` / ajusten `pos["sl"]`, con LOCK de `arena`.
- Hay botones parecidos ya en `oficina3d.html` para Julián (proteger/cerrar): reutilizar el patrón.

## 3. Resumen y ranking de estrategias
- Pestaña/apartado «Ranking»: mejores y peores estrategias (por neto, y por R medio, win-rate, nº de ops, drawdown), por mercado y para la cuenta propia. Usa `arena.json` (e["neto"], e["n"], e["cerr"]).
- Mostrar también la nueva métrica **mfe** (hasta dónde llegó a favor cada operación, en R; ya se guarda en cada trade cerrado desde 2026-10-13) para decidir salidas: break-even a +0,7 R, toma parcial a +1 R, o cierre total.

## 4. Análisis de la toma de ganancia (pendiente)
- Con ≥50 operaciones cerradas con `mfe`: calcular % que llegó a +0,5/+0,7/+1 R, y cuántas de esas terminaron en SL. Comparar reglas: BE a +0,7 R, parcial a +1 R, cierre total corto. Reportar costo (comisión+slippage) incluido.

## 5. Protección del flotante (pedido 2026-10-13)
La dueña vio el flotante total de Futuros llegar a ~$1000 y bajar a ~$200. Quiere poder cerrar cuando el flotante del momento es bueno y/o cuando una operación ya va en positivo (idea: ~$50). Diseño propuesto (a confirmar con ella):
- (a) Botones manuales Proteger/Cerrar (ya en §2) — prioridad 1.
- (b) Salida automática por posición: break-even a +0,7 R y/o trailing (ya existe trailing en `salida_pos`); NO un objetivo fijo de $50 si el stop puede ser hasta $500 (exigiría ~91 % de aciertos).
- (c) **Trailing del flotante total** por mercado/cuenta: si el flotante agregado cae X % (p. ej. 40 %) desde su pico (con pico mínimo p. ej. $300), cerrar todo o proteger todo. Es lo que habría evitado $1000→$200. Parámetros editables, con aviso a Discord.

## 6. ORDEN DE TRABAJO ACTIVA (2026-10-13, la dueña dijo «hazlo», con uso extra pagado): panel interactivo DENTRO de /iso2
Hecho ya en `arena.py`: break-even a +0,7 R (`BE_R`), `proteger_flotante`, campo `mfe` en cada trade, horario Futuros dom 18:00–vie 15:15. Construir ahora (versión mínima, por pasos, con respaldo `.bak-panel` antes de editar):
1. **Backend** (`arena.py` + `server.py`, patrón de rutas existentes, JSON, con `arena.LOCK`):
   - `GET /api/arena/resumen` → por mercado: lista de estrategias (id, nombre, trader, creador, tf, sl_atr, tp_atr, trail, ops, ganadas, conteo de tp/sl/trailing/tiempo, neto, R medio, mfe medio, abiertas, estado, clase) + mejores/peores 5 + en Futuros las cuentas (n, saldo, pico, ops, fondeadas, quemadas).
   - `GET /api/arena/abiertas` → posiciones abiertas con estrategia, símbolo, lado, entrada, precio actual (`pos["px"]`), SL, TP, flotante USD (`arena._flot_usd`), minutos abierta.
   - `POST /api/arena/accion` `{accion, id, i?, mercado?}`: `proteger` (SL a break-even +0,1 R, solo si va en ganancia), `cerrar` (cierra esa posición al precio `px` con motivo nuevo `"manual"`; añadir `manual` al dict `ic` de `cerrar_pos`), `cerrar_todas` (de un mercado), `pausar`/`reanudar` (estado `pausada`; `activas()` solo toma `activa`) y `retirar` (a basura con razón «retirada manual»). SOLO afecta la arena simulada; nunca ordenes reales (Bitunix real no está activado; no tocar la demo de AMP de Julián).
2. **UI en `static/iso2.html`** (reusar los docks de Futuros/Bitunix y su 4 pestañas): pestaña «Estrategias» = tabla ordenable por columna con filtro Bitunix/Futuros y columnas SL×ATR, TP×ATR, ops, TP/SL/Trail/Tiempo, neto, MFE; filas con botones (Pausar, Retirar, Ver operaciones); bloque «Mejores / Peores»; pestaña «Cuentas» (Futuros: cuentas por estrategia con saldo, pico, ops, fondeadas/quemadas); pestaña «Abiertas» con botones 🛡 Proteger y ✖ Cerrar por posición y «Cerrar todas» (confirmación `confirm()` en cerrar_todas y retirar). Refresco cada 5 s. Colores: verde ganancia, rojo pérdida.
3. Verificar con consola/JS (no capturas) y con un test que cierre una posición simulada de prueba en una copia de `arena.json` (no en el real). Reinicios: no reiniciar runner/servidor; avisar a Claude para que lo haga.
4. Pendiente aparte (avisar, no arreglar sin permiso): hay 95 estrategias activas en Futuros y 86 en Bitunix aunque el tope es 50 por mercado; investigar en `revision.py::cupos`.

## 7. ORDEN ACTIVA (2026-10-13): CUENTA PROPIA de $200 con E-nanos (la dueña: «pendiente, por qué? hazlo»)
Panel §6 ya terminado y desplegado (colas `arena_acciones.jsonl`, hilo `acciones`, rutas `/api/arena/*`). Ahora construir la **cuenta propia**, reutilizando esa infraestructura:
- **Estado** en `arena.json` clave `S["propia"]`: saldo inicial 200 USD, pico, pos (lista), cerr (≤200 recientes), neto, n, ganadas, estado ("activa" | "agotada" si saldo < 20), `feed` (ids de estrategias que la alimentan), `com_nano` (comisión USD por contrato y lado; parámetro, **por defecto 0,25** hasta que la dueña dé la real) y slippage 1 tick por lado.
- **Sin reglas de fondeo:** sin tope diario, sin «quemada». Máx **3 nanos abiertos en total**. Riesgo por operación = 3 % del saldo (parámetro `riesgo_pct`); tamaño = floor(riesgo / (dist × valor_punto_nano)), mínimo 1, máximo 3 (si 1 nano ya excede 6 % del saldo, se omite la señal).
- **Valores por punto (tabla CME E-nano):** MES→NES $0,50, MNQ→NNQ $0,20, MYM→NDOW $0,05. **MGC no aplica** (no hay nano de oro). Mismos precios/datos de AMP (MT5) que Futuros.
- **Alimentación:** las 5 mejores estrategias de Futuros por neto con ≥30 operaciones cerradas (recalcular cada hora; mostrar cuáles son), más las que la dueña fije a mano. Cuando una de ellas abre en la arena de Futuros, la cuenta propia **replica** la entrada (mismo lado, SL, TP, trailing) si hay cupo (≤3 nanos, 1 posición por activo). Salidas con `salida_pos` (incluye break-even a +0,7 R y la protección del flotante). Mismo horario de Futuros (dom 18:00–vie 15:15, plano 15:30).
- **Controles:** pestaña «Cuenta propia» en los docks de `iso2.html` (saldo, pico, neto, ops, curva simple, posiciones abiertas con 🛡 Proteger / ✖ Cerrar / Cerrar todas, lista de estrategias que la alimentan con opción de agregar o quitar, y campo editable de comisión y de riesgo %). Acciones nuevas en `/api/arena/accion` con `mercado:"propia"`.
- **Discord:** avisos de la cuenta propia al canal de Futuros con prefijo «🧾 CUENTA PROPIA».
- Es SIMULADA (no hay broker conectado). Nunca órdenes reales. No tocar la demo de AMP ni stops de Julián.
- Respaldos `.bak-propia` antes de editar; probar sobre una COPIA de `arena.json`; no reiniciar (avisar).

## 8. ORDEN ACTIVA (2026-10-13): «Cerrar contrarias» + regla opcional + «fantasma» para medirla
Caso de la dueña: en un mismo activo hay compras y ventas abiertas a la vez (cada estrategia es independiente); si un lado va muy ganador, el opuesto (perdedor) se come ganancias. Construir sobre la infraestructura de acciones ya existente (cola `arena_acciones.jsonl`, hilo `acciones`, `/api/arena/accion`, pestaña Abiertas de `iso2.html`):
1. **Botón** en Abiertas: barra por activo que tenga posiciones en ambos lados, con texto tipo «MYM: 3 compras (+318) · 1 venta (−195)» y botones **«Cerrar contrarias»** (cierra el lado perdedor del activo) y «Cerrar ventas»/«Cerrar compras». Acción nueva `cerrar_lado` `{mercado, sym, lado}`; usa `cerrar_pos` con motivo `manual`; en Futuros rechaza si no hay precio (fuera de horario). No aplica a la cuenta propia (ya permite 1 posición por activo).
2. **Fantasma:** al cerrar contrarias (manual o por regla), guardar en `S["fantasmas"]` la posición cerrada (est, sym, d, ent, dist, sl, tp, trail, peak, usd_cierre, t_cierre) y SEGUIRLA solo en el registro (mismas salidas `salida_pos` y mismo modelo de costos, sin tocar saldos) hasta que termine; al terminar guardar `usd_final` y `ahorro = usd_cierre - usd_final` (positivo = cerrar valió la pena). Exponer en `/api/arena/resumen` un bloque `contrarias`: casos, balance total (suma de ahorros), % de casos en que valió la pena, y la lista de los últimos 20. Mostrarlo como pequeña estadística en la barra de Abiertas.
3. **Regla automática, APAGADA por defecto** (`S["cfg"]["auto_contrarias"] = False`, interruptor en la UI): por mercado, si un activo tiene un lado con flotante ≥ umbral (Futuros 150 USD, Bitunix 5 USD; editable) y el lado opuesto suma flotante negativo, cerrar el opuesto (con fantasma y aviso a Discord «🤝 contrarias cerradas»). Enfriamiento de 10 min por activo.
4. No tocar la lógica de cada estrategia ni Bitunix real ni la demo de AMP. Respaldos `.bak-contr`; pruebas sobre COPIA de `arena.json`; sin capturas; no reiniciar (avisar qué).

## Bitácora
- 2026-10-13 (Claude, orden §6 ejecutada). Respaldos: `Agentes/_archivo_viejo/{arena.py,server.py,iso2.html}.bak-panel`.
  - `arena.py`: motivo `manual` en `cerrar_pos`; funciones `resumen`, `abiertas`, `ops_de`, `aplicar_accion` (proteger/cerrar/cerrar_todas/pausar/reanudar/retirar) y `procesar_acciones`; hilo nuevo `acciones` (cada 1 s).
  - Diseño: runner y servidor son procesos distintos. El servidor NO toca la arena: lee `arena.json` (GET `/api/arena/resumen|abiertas|ops?id=`) y encola las acciones en `arena_acciones.jsonl` (POST `/api/arena/accion`); el runner las aplica y responde en `arena_acciones_res.json`. Sin runner vivo, la acción queda en cola y el servidor avisa a los 6 s.
  - `iso2.html`: pestañas Estrategias (ordenable, filtro de mercado, mejores/peores 5, Pausar/Retirar/Operaciones), Cuentas (Futuros) y Abiertas con Proteger/Cerrar/Cerrar todas; refresco 5 s.
  - Límites: `px` solo se actualiza con mercado/ciclo activo (Futuros fuera de horario no tiene precio: cerrar/pausar se rechazan). Conteos TP/SL/Trail/Tiempo salen de las últimas 120 ops guardadas. Pausar y Retirar cierran las posiciones al precio actual y liberan cupo (entra una «aprobada»).
  - Prueba sobre COPIA de arena.json: OK (proteger, cerrar manual, pausar/reanudar, retirar, cerrar_todas, ruta POST+cola y UI por JS sin errores de consola). Falta: reiniciar runner (hilo nuevo y motivo manual) y servidor.
  - Hallazgo §6.4: no hay exceso. 95/86 = activas + «aprobadas» en espera. Activas: 50 Futuros y 50 Bitunix exactamente; 45 y 36 aprobadas esperan cupo (`revision.py::cupos` respeta `MAX_ARENA`).
- 2026-10-13 (Claude, orden §7 ejecutada). Respaldos: `Agentes/_archivo_viejo/{arena.py,server.py,iso2.html}.bak-propia`.
  - `arena.py`: estado `S["propia"]` (200 USD, feed_auto/feed_man/feed_off, com_nano 0,25, riesgo_pct 3); `propia_copiar` (replica entradas de las 5 mejores de Futuros con ≥30 ops, recalculo horario, + manuales; E-nanos NES/NNQ/NDOW, máx 3 nanos, 1 por activo, omite si 1 nano > 6 % del saldo), `propia_salidas` (dentro de `ciclo_fut`, con BE a +0,7 R y trailing), `propia_cerrar` (comision + 1 tick por lado), `proteger_flotante("propia")`, `propia_accion` (proteger/cerrar/cerrar_todas con `mercado:"propia"`, `propia_feed_add/del`, `propia_cfg`), `propia_vista`. Estado «agotada» si saldo < 20. Avisos a Discord Futuros con «🧾 CUENTA PROPIA».
  - `server.py`: GET `/api/arena/propia`; POST `/api/arena/accion` acepta las acciones nuevas (campos sid, com_nano, riesgo_pct).
  - `iso2.html`: pestaña «Cuenta propia» en el dock de Futuros (saldo, pico, neto, curva, abiertas con Proteger/Cerrar/Cerrar todas, feed con Quitar/Agregar, comision y riesgo % editables, últimas ops).
  - Prueba sobre COPIA de arena.json y JS por node: OK. Falta reiniciar runner y servidor. Hoy solo 2 estrategias de Futuros tienen ≥30 ops, así que el feed arranca con pocas.
- 2026-10-13 (Claude, orden §8 ejecutada). Respaldos: `Agentes/_archivo_viejo/{arena.py,server.py,iso2.html}.bak-contr` (un intento previo murió por límite de API sin editar; verificado idénticos antes de empezar).
  - `arena.py`: `cerrar_lado` (compra/venta/perdedor; motivo manual; Futuros rechaza fuera de horario), `S["fantasmas"]` + `fantasmas_paso` (seguidos en `ciclo_bx`/`ciclo_fut` con `salida_pos` y mismo costo, sin tocar saldos; guardan `usd_final` y `ahorro`), `contrarias_stats` (bloque `contrarias` en `/api/arena/resumen`: casos, balance, % valió, últimos 20, auto, umbral), `auto_contrarias` (APAGADA por defecto, `S["cfg"]["auto_contrarias"]`, umbral Futuros 150 / Bitunix 5, enfriamiento 10 min, aviso Discord «🤝 contrarias cerradas»), acciones `cerrar_lado` y `contr_cfg`.
  - `server.py`: solo la lista blanca de acciones y campos (sym, lado, auto, umbral).
  - `iso2.html`: barra por activo con compras y ventas en «Abiertas» (Cerrar contrarias / ventas / compras, confirm), estadística de contrarias, interruptor de la regla y umbral editable.
  - Prueba sobre COPIA de arena.json (cerrar_lado ambos mercados, fantasma hasta fin, ahorro, regla auto con enfriamiento, resumen) + JS por node: OK. Falta reiniciar runner y servidor.
