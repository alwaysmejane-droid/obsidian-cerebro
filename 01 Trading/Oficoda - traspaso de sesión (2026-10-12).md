# Traspaso de sesión — 2026-10-12
_Léelo al empezar la sesión nueva. Resume todo lo acordado y el estado real._

## Estado hecho y funcionando
- **Arena** (50+50 estrategias, demo simulada) corriendo en el runner: `Agentes/arena.py`, `vivo.py`, `revision.py`, `creadores.py`, `paneles.py`. Bitunix $200 virtuales/estrategia; Futuros cuentas 25k simuladas, 1-3 micros, cierre 3:30 PM, Bitunix máx 24 h. 19 trabajadores (ver `Agentes/EQUIPO_REFORMA.md`).
- **Costos Bitunix** en la arena: comisión 0,09 %/lado (0 en pares cero-fees: SOL, XRP, DOGE, CL, BZ, XAG, XAU), slippage 0,0195 %/lado y **medio spread real del libro** (depth) desde hoy. Spread real medido ≈ 0,0001–0,005 %: ya estaba cubierto. Funding no se cobra.
- **Discord**: avisos en recuadros (embeds) con color y emoji: Bitunix → #bot-bitunix, Futuros → #bot-indices-thewhales; resumen cada hora. Webhooks se leen de los .env, nunca se imprimen.
- **Contenido para creadores**: `Agentes/biblioteca.py` (búsqueda web DuckDuckGo + lectura de la carpeta `PROYECTO/Libros`, acepta .pdf/.txt/.docx; indicadores de TradingView como .txt) → fichas (`doc="idea"`) → Yaima → revisión → arena.
- **Taller gratis**: `Agentes/delegar.py` (modelos OmniRoute: kimi-k2.7-code, deepseek-v4-pro, glm-5.2, gpt-oss-120b…). En la práctica falló con la escena 3D (6 modelos); funcionó con el muñeco.
- **CLAUDE.md** en la raíz + agentes `.claude/agents/` (explorador Haiku, redactor Sonnet, revisor Sonnet).
- Páginas: `/maqueta` (maqueta 2D animada, muñecos), `/prueba` (prueba 3D aprobada «no está mal»: muñecos con manos/pies, pelo variado, plantas), `/3d2` (oficina v2 del sub-agente: 8 salas-cápsula, 19 trabajadores, escritorios, funcional conectado). La oficina real (`/` y `/3d`) NO se ha tocado.

## Pendiente principal: rediseño 3D estilo Los Sims
Ver «DIRECCIÓN v2» en `Cerebro/01 Trading/Oficoda - plan 3D nuevo.md`. La dueña dijo que `/3d2` «no está mal pero no es el flujo unido ni el diseño que describimos» y **va a pasar una FOTO de referencia**: lo primero es ver la foto, decidir qué copiar (distribución / estilo / ambos) y mostrar una maqueta estática ANTES de construir en la oficina real.
Ideas ya pedidas: una sola oficina tipo Sims; zonas: descanso (café, radio, muebles), sala de reunión (8:00 caminan todos), cada departamento con escritorios, silla gamer, monitores curvos, decoración; muñecos redondos con manos y pies, ropa y pelo distintos; paneles que se recogen con toda la info acordada (Arena en tabla ordenada por neto, Abiertas, Señales, Registro, Personas, Salud, Buzón, Marisol, reporte 8:00, costos); menú corto (Arena · Personas · Salud · Buzón · Marisol · Vista ▾ · Más ▾); docks no deben abrir por defecto tapando pantalla. Faltan en /3d2: vida social (café, reunión, baile), vistas "Un puesto/Zona de trabajo/Descanso" más precisas, rendimiento.

## Otros pendientes
- Voz: hoy voces del navegador (hash por nombre). Ofrecido: selector de voz por trabajador (recordado) y/o voces neuronales de Edge. Sin decidir.
- Ordenar la arena: un solo panel con tabla (nombre, creador, mercado, ops, neto, estado), orden por neto, filtro Bitunix/Futuros. Sin permiso aún para hacerlo.
- Confirmar que los avisos de Discord caen en los canales correctos y que el nuevo formato de recuadros le gusta.
- Primeros cierres/resumen horario de la arena: verificar.
- Admin `powercfg /requests` por si el PC se duerme y causa las caídas diarias (sin ejecutar).

## Límite de uso (dueña)
Reserva ≥5 % hasta mañana; parar antes del 90–95 %. A las 16:00 UTC 5h al 73 %, semanal 79 % (se reinicia 2026-10-13 22:00 UTC aprox.). Sesión nueva = no arrastrar 170 k tokens; delegar con los agentes y los modelos gratis; Grep en vez de leer archivos enteros.
