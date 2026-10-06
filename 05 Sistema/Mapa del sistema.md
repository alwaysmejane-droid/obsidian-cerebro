# Mapa del sistema (todo corre en mi PC)

Un supervisor (`supervisor.py`, carpeta PROYECTO) arranca y vigila los servicios.

| Servicio | Qué es |
|---|---|
| open30 | Estrategia [[Open30 (MNQ)]] en vivo, señales + Discord |
| mnq-gate | Puerta/acceso del dashboard de MNQ |
| kalshi-dash / kalshi-bot / kalshi-lab | [[Kalshi]]: panel, bot y laboratorio demo |
| bitunix-lab | [[Bitunix]]: laboratorio paper + operación real en XRP |
| comidas / comidas-gate | App de [[Comidas]] |
| tony / ngrok-tony | Bot de [[Tony]] (detenido) |

## Acceso
- Dashboard: por Tailscale, `https://mas53.tail13b7ee.ts.net` (sin puerto).
- Control del supervisor: `http://127.0.0.1:8766/` con cabecera `X-Ctl: 1` y acciones estado / iniciar / parar / reiniciar.

## MetaTrader 5
- Terminal en Program Files = hora de NY exacta (usar este para Open30 y los indicadores).
- `thewhale` abierto; `open15` y `tony` cerrados.

Ver [[Cómo parar cosas]].
