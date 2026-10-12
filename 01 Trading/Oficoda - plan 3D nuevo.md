# Oficoda 3D nueva — especificación y bitácora de trabajo
_Fuente de verdad para los sub-agentes. Quien trabaje lee SOLO este archivo + los archivos que cita, y al terminar anota abajo en «Bitácora». Creado 2026-10-12._

## Objetivo
Misma oficina 3D que ya existe (`Agentes/static/oficina3d.html`, servida en `/` y `/3d`) con diseño nuevo y los 19 trabajadores del equipo reformado (ver `Agentes/EQUIPO_REFORMA.md` y `Agentes/agentes.json`). La versión nueva se construye en **`Agentes/static/oficina3d_v2.html`** y se sirve en **`/3d2`** (NO reemplazar la actual hasta que ella lo apruebe).

## Decisiones de la dueña (no cambiar)
- Estilo: muñecos redondeados y coloridos CON manos y pies, ropa distinta cada uno, pelo con detalle (corto, largo, rizado, moño, coleta, calvo+barba). Referencia aprobada: `Agentes/static/prueba3d.html` (url `/prueba`): salas con paredes redondeadas y borde luminoso, anillo de Arena que gira, monedas, plantas, ficus, libreros, pizarras, relojes, cuadros, dispensador, café con vapor, radio con notas, Chencho caminando.
- Ahora SÍ cada persona en su **escritorio real** (en la maqueta anterior se quitaron; ahora vuelven, bonitos y redondeados, con pantalla/lámpara/taza). Solo los 19 + ambiente (limpieza Chencho, música, café). **Nada de personajes viejos** (los de la oficina antigua de 33).
- Un departamento = una sala con su nombre y color. Salas (ids de `DEPTOS` en `Agentes/server.py`): direccion (Marisol), ideas (Yaima), creacion (Raúl, Yoel, Pepito), revision (Ofelia, Gaspar), operacion (Lázaro, Valentín, Zoila, Julián), registro (La Caridad, Mercedes, Migdalia), datos (Mireya, Rolando), archivo/ambiente (Cheo, Ñico, Chencho). En el centro la **Arena** (anillo, monedas).
- Debe conservar TODO lo funcional de la oficina actual: llamadas a la API (`/api/...`), estado de cada trabajador (luz verde=trabajando, amarilla=espera/alerta, etc.), clic en un trabajador abre su ficha/chat, botón Marisol, voz (🔊 🎤 ▶ Reunión 8:00), docks de Futuros/Bitunix/Arena, cámaras, Noche/Ahorro.
- Menú superior corto (ver `Agentes/static/maqueta3.html` en `/maqueta`): Arena · Personas · Salud · Buzón · Marisol · Vista ▾ · Más ▾ (Vista = las 6 cámaras y Girar; Más = Radio, Noche, Ahorro, Embudo, Bitácora, Candidatas, Estrategias, Recomendaciones, En vivo, Operaciones).
- La escena queda rodeada de paneles (docks arriba/abajo, laterales) que se pueden recoger: encuadrar la cámara para que se vea bien con los paneles abiertos y llene la pantalla con ellos recogidos. Responsive.
- Rendimiento: ligero (el PC lo usa a diario). Modo Ahorro baja la calidad y la tasa de cuadros.
- Pelo, ropa y rasgos fijos por persona (tabla abajo).

## Trabajadores (id de agentes.json → aspecto)
| id | nombre | depto | aspecto |
|---|---|---|---|
| jefa | Marisol | direccion | camisa naranja, corbata amarilla, moño |
| fut2 | Yaima | ideas | camisa violeta, pelo largo oscuro, gafas |
| inv3 | Raúl | creacion | camisa azul, gafas, pelo corto castaño |
| inv1 | Yoel | creacion | camisa verde menta, corbata roja, rizado |
| est1 | Pepito | creacion | camisa amarilla, gorra roja, pelo corto |
| esc_pbx | Ofelia | revision | camisa rosa-roja, coleta, gafas |
| esc_pfut | Gaspar | revision | camisa azul petróleo, pelo gris corto |
| paper1 | Lázaro | operacion | camisa naranja, corbata negra, pelo corto |
| firmas | Valentín | operacion | camisa turquesa, pelo negro corto |
| fut4 | Zoila | operacion | camisa roja, pelo largo negro |
| fut_demo | Julián | operacion | camisa azul acero, pelo castaño rizado |
| esceptico | La Caridad | registro | camisa fucsia, moño |
| fut_dest | Mercedes | registro | camisa celeste, coleta |
| paper2 | Migdalia | registro | camisa verde claro, pelo corto |
| datos | Mireya | datos | camisa amarilla, pelo largo |
| fut1 | Rolando | datos | camisa verde, pelo corto |
| vigilante | Cheo | archivo | camisa azul petróleo, gorra, silbato |
| archivista | Ñico | archivo | camisa rojo-rosa, calvo con barba, gafas |
| est2 | Chencho | ambiente | delantal blanco, gorra azul, camina limpiando |
(Si algún id difiere en `agentes.json`, manda `agentes.json`.)

## Reglas de trabajo para sub-agentes
- Leer solo lo necesario (usar Grep, no leer archivos enteros de 600+ líneas).
- No tocar `server.py` salvo añadir la ruta `/3d2` (copiar el patrón de `/prueba`). No reiniciar servicios sin avisar.
- Three.js r128 desde unpkg (igual que `oficina3d.html`).
- Verificar: abrir `http://127.0.0.1:8797/3d2` en el navegador del panel, leer errores de consola, contar personas con JS. Los screenshots del 3D se cuelgan: NO usarlos.
- No imprimir ni pedir claves. Python 3.14, PowerShell 5.1 (sin `&&`).
- Anotar al final de este archivo qué hizo y qué falta.

## DIRECCIÓN v2 (2026-10-12, PREVALECE sobre lo anterior en distribución y estilo)
La dueña pidió estilo **Los Sims**: UNA sola oficina/edificio vista en ángulo (cámara isométrica-ish, con vistas), NO cápsulas sueltas flotando:
- Planta única con suelo (madera/alfombra por zona), paredes bajas o con cristal que separan zonas, ventanas, puertas. Se ve como una casa de muñecas / Sims, con corte para ver dentro.
- **Zonas:** (1) área de descanso: cafetera/barra de café, radio con música, sofás, puffs, mesa baja, planta, máquina de snacks, dispensador; (2) **sala de reunión** con mesa grande y sillas (ahí se «sientan» a las 8:00 cuando corre ▶ Reunión: los 19 caminan a la sala); (3) un área por departamento con su rótulo; (4) la Arena en un espacio central/destacado (anillo, monedas, pantalla grande con el neto del día).
- **Escritorios** reales por persona, con **silla gamer** (respaldo alto, reposacabezas de color), **monitor curvo** (o dos), teclado, ratón, taza, lámpara; el color de la silla acompaña al de su ropa. Los monitores muestran algo que cambia con el estado (verde=trabajando).
- Decoración rica: plantas, cuadros, estanterías, alfombras, lámparas de pie, pósters, reloj, cortinas; luces cálidas. Colorido y bonito.
- Los muñecos siguen redondeados, con manos y pies; se mueven: sentados trabajando (tipeo), levantarse e ir al café, caminar a la reunión; Chencho limpia.
- **Paneles (docks) que se recogen**, laterales/arriba/abajo, pero con TODA la información acordada: Arena (tabla ordenada por neto, filtro Bitunix/Futuros), Abiertas, Señales, Registro, Personas, Salud, Buzón, Marisol, reporte de las 8:00, Costos. El menú superior corto (ver arriba). Recogidos, la escena llena la pantalla.
- Ya no hay «ocho cápsulas»: el esquema por salas se conserva solo como zonas dentro del mismo edificio.

## Fuentes de assets 3D aprobadas
- **Kenney.nl** — assets CC0, descarga con Invoke-WebRequest.
- **poly.pizza** — modelos GLB/GLTF CC0 (oficina, sillas, escritorios, plantas, personajes). Buscar: "office", "desk", "chair", "character". Descargar igual que Kenney. Usar donde haya mejor calidad o variedad.

## Bitácora
- 2026-10-12 (sub-agente v2): creado `Agentes/static/oficina3d_v2.html` (ruta `/3d2` añadida en server.py antes de `/prueba`; requiere REINICIAR server.py para verla en 8797).
  - Se genera con `Agentes/static/v2/ensambla.py` (une CSS/paneles/lógica de oficina3d.html + `v2/personas_A1.js` + `v2/escena_v2.js`). Editar esos archivos y volver a ejecutar `python ensambla.py`.
- 2026-10-12 (sub-agente redactor): reescrito `Agentes/static/v2/escena_v2.js` con layout de oficina real conectada: suelo base rectangular (95×85) con pasillo central, 8 zonas de trabajo con paredes bajas (2.6 alto) y bordes neon emissive por color de departamento, coordenadas ampliadas (x=±30, z=±25/0), +2 zonas sin trabajadores: DESCANSO (sofás, cafetera, radio) y REUNIÓN (mesa oval, 8 sillas, TV). Arena central con 12 monedas, PointLight magenta. Toda la lógica (ASP{}, ROOMS[], estados, animate, click, STEAM, NOTAS, Chencho) conservada intacta. `ensambla.py` genera OK (88 084 chars). Falta: reiniciar server.py para ver en /3d2.
  - Taller gratis: `personas_A1.js` (muñeco makePerson) lo redactó cerebras/gpt-oss-120b (con arreglos a mano: postura sentada). La tarea B (salas/arena) falló en los 6 modelos (KeyError) y se escribió a mano (`escena_v2.js`: sillas, escritorios redondeados con pantalla/taza/lámpara, 8 salas, Arena, buzón, radio con notas, cafetera con vapor, Chencho barriendo).
  - HECHO: 19 personas (18 sentadas + Chencho caminando), 8 salas con rótulo clicable (chat del supervisor), luz por estado (verde trabajando, amarilla espera/alerta, Zzz y "!"), pantallas con velas, Arena con texto de datos reales, pizarra de Marisol, menú corto (Arena, Personas, Salud, Buzón, Marisol, Vista▾, Más▾), todas las APIs/paneles/chat/voz/docks/radio/Noche/Ahorro heredados de la oficina actual, encuadre automático según paneles abiertos, comprobado sin errores en consola (19 personas, 8 salas, 1356 mallas).
  - FALTA: revisión visual de la dueña (no se hicieron capturas; el panel estaba oculto); ajustar posiciones/colores; la vida social antigua (paseos, reuniones, baile, café en grupo) NO se portó: solo Chencho camina; `celebrate` solo acelera las monedas; los docks Futuros/Bitunix abren por defecto (como en la actual); vistas "Un puesto/Zona de trabajo/Descanso" son aproximadas; sin rendimiento medido (1356 mallas).
  - PENDIENTE por «DIRECCIÓN v2» (recibida al terminar): la distribución actual sigue siendo las 8 cápsulas. Falta rehacer `escena_v2.js` como UNA planta tipo Sims (suelos por zona, paredes bajas/cristal, ventanas, sala de reunión con mesa, área de descanso con sofás/puffs/snacks, Arena central con pantalla del neto), sillas gamer con respaldo alto y monitor curvo, más decoración, y portar la vida (levantarse al café, caminar a la reunión de las 8:00, Chencho). Reaprovechables tal cual: `makePerson` (personas_A1.js), tabla ASP de aspectos, estaciones/estados/luz, encuadre por paneles, menú y toda la lógica de API. Los helpers de decoración y `ensambla.py` también sirven.
- 2026-10-12 (sub-agente redactor 3): creado `Agentes/static/oficina2d.html` — diorama isométrico 2D con Canvas2D. Proyección toScreen(wx,wy,wz) con TW=56/TH=28/TY=42, painter's algorithm (sort por wx+wz), 11 zonas (9 con trabajadores + descanso + reunion), 19 muñecos cartoon con cabeza grande/brazos animados/luz de estado, Arena con anillo giratorio y 12 monedas orbitando, cafetera con vapor, notas musicales, mesa de reunión oval, TV, plantas, etiquetas de zona. Drag para mover la vista, scroll para zoom, click en muñeco abre su ficha, hover muestra tooltip. Conecta a /api/estado cada 8 s. Sin reiniciar server.py (archivo estático). FALTA: revisar visual en navegador (la dueña); añadir modo Ahorro y voz; integrar docks de Futuros/Bitunix; más decoración por zona.
- 2026-10-12 (sub-agente redactor — mejoras visuales oficina2d): aplicado en `Agentes/static/oficina2d.html`: TH=20/TY=38/origen cv.height*0.35 (vista más frontal), shadeCol(), sillas gamer con respaldo alto+alas+apoyabrazos+cabecero, monitor curvo con texto de datos y glow, tablero madera clara, 3 tipos de plantas (monstera/cactus/flores), ventanas animadas en paredes exteriores (drawWindows), carteles de zona con fondo de color, área descanso con sofás gamer+cafetera premium LED+frigorífico+estante, sala reunión con 8 sillas+pantalla grande+whiteboard, pantallas LIVE DATA en zonas datos/operacion, segunda planta por zona. Estilo claro: fondo #e8edf4, paredes crema, piso madera cálida, divisiones de vidrio semitransparente (drawWallNGlass/drawWallWGlass). FALTA: revisión visual en navegador.
- 2026-10-12 (sub-agente redactor — actualización index.html): actualizados los 19 trabajadores en `Agentes/static/index.html`. Reemplazados ZONAS (8 nuevas: direccion/ideas/creacion/revision/operacion/registro/datos/archivo), ESTACIONES (19 posiciones), PERSONAS (colores/pelo/piel), FIJOS, VIEWS (9 vistas). Agregado CHENCHO_PATH + chenchoState() para que est2/Chencho recorra los pasillos. Secciones renderSide actualizadas con nombres nuevos. No se tocó el código de dibujo, diálogos ni controles.
- 2026-10-12 (sub-agente redactor 2): reescrito `escena_v2.js` completo como planta única tipo Sims/dollhouse. Cambios principales: suelo madera cálida unificado (115×100), 8 zonas con PlaneGeometry alfombra de color pastel (28×24), paredes bajas h=2 color 0xf0ebe0 (no neon), muñecos reemplazados por `makePersonMario()` (cabeza grande 0.55, torso gordito, piernas/brazos cortos y gruesos, ojos/nariz, gorra/gafas opcionales), sillas `makeChairMario()` con CapsuleGeometry, escritorios con 4 patas cilíndricas y madera 0xc4956a, Arena central (radio=12, z=0) con anillo grande y 12 monedas a r=7.5, DESCANSO (x=-20,z=50) y REUNIÓN (x=20,z=50) en fila extras con paredes pastel, iluminación cálida (AmbientLight 0xfff5e4 en panel base, bulbo techo emissive por zona), layout corregido (ROOMS x=±35, z=-30/0/30). ASP{} y toda la lógica conservada. `ensambla.py` OK (90013 bytes). FALTA: reiniciar server.py para ver en /3d2; validar visual en navegador.
