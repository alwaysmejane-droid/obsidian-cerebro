# Cómo trabajar en la Oficoda (agentes y ahorro de límite)
_Se lee SOLO cuando hace falta; `CLAUDE.md` apunta aquí._

## Plan vigente
- Plan maestro con los pasos 0-13 y las decisiones: [[Oficoda - plan maestro fondeo]]. MES y MGC fuera de pruebas y fondeo; trabajo con MNQ y MYM.
- Estado y pendientes de la sesión anterior: [[Oficoda - traspaso de sesión (2026-10-12)]]. Plan de la cuenta propia/botones/contrarias: [[Oficoda - plan cuenta propia + botones + ranking]].

## Agentes (`.claude/agents/`)
| Agente | Modelo | Dueño de | Para qué |
|---|---|---|---|
| explorador | Haiku | nada (solo lee) | buscar y resumir |
| analista | Haiku | `Cerebro/.../Arena - Análisis.md` | estadísticas y calificaciones (scripts) |
| motor-fondeo | Sonnet | `Agentes/arena.py` | pasos 0-6 del plan |
| panel-whales | Sonnet | `Agentes/static/iso2.html` | dashboard The Whales Office |
| backtester | Sonnet | `Agentes/backtest_min.py` | backtest mínimo (últimas 50 sesiones, costos reales) |
| redactor / revisor | Sonnet | – | construir / probar |

## Método para gastar poco
1. El coordinador decide el paso, lanza **un** agente con la sección del plan y lee solo su informe (≤10 líneas).
2. Los agentes leen **su** sección del Cerebro, no la conversación; anotan al final en «Bitácora».
3. Lo repetitivo corre en scripts y en la IA gratis (OmniRoute): analista/ajustador/gestor dentro de la Oficoda no usan Claude.
4. Sesión nueva por fase; modelo Sonnet para coordinar. No releer código: Grep y lecturas parciales.
5. Un dueño por archivo (evita choques entre agentes). Reinicios: matar proceso, el vigilante relanza (~90 s).
