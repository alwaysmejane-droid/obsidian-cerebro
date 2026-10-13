# Traspaso de sesión — Oficoda 2D (2026-10-12b)

## Estado actual
- `Agentes/static/oficina3d.html` reescrito en **Canvas 2D** (sin Three.js).
- Carga en el servidor 8797, zonas visibles, muñecos animados funcionando.
- **Problema**: diseño feo — ventiladores parecen X, muñecos muy pequeños, colores apagados.
- La dueña dice "horrible todo" y quiere rediseño completo.

## Plugin disponible
**AnimatedWebs** (ya instalado, necesita sesión nueva para cargar):
- `/design` — estilos visuales
- `/component` — componentes animados
- Úsalo para generar CSS/Canvas con estilo cinematográfico bold.

## Lo que debe mejorar
1. Muñecos pixel-art más grandes, con caras, cabello, expresión
2. Zonas con piso texturizado (no solo color plano)
3. Arena con efectos de rayos/electricidad
4. Quitar ventiladores o hacerlos visibles de verdad (no X's)
5. Lámparas colgantes que se vean bonitas
6. Colores más vivos y contrastados
7. Sala de reuniones visible (no tapada por header)

## Layout aprobado (no cambiar)
- Columna izq: DIR, REV, REG
- Centro: ARENA (grande) + DESCANSO abajo
- Columna der: IDEAS+DATOS, TRADERS, VIG+ARCH, ESCÉPTICOS
- Sala reuniones: franja superior full-width

## Agrupaciones (no cambiar)
- Ñico (archivista) + Cheo (vigilante) → zona VIG+ARCH
- Yaima (fut2) + Rolando (paper2) + Mireya (datos) → zona IDEAS+DATOS

## Segundo script (líneas 729+)
NO tocar — es el dock de Futuros/Bitunix, funciona bien.
