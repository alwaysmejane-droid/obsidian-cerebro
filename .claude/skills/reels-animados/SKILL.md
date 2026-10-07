---
name: reels-animados
description: Crea reels cortos verticales (9:16, 15-30 s) en MP4 para Instagram usando ffmpeg y Python. Úsala cuando la usuaria pida un reel, video corto, TikTok o contenido para Instagram, especialmente del canal "La fresa y la naca" con las perritas Popi (pitbull mix, la naca) y Luna (shih tzu, la fresita).
---

# Skill: reels-animados

Crea reels verticales MP4 (1080×1920, 30fps) usando `~/.claude/skills/reels-animados/scripts/crear_reel.py` y ffmpeg.

## Contexto del canal

- **Canal:** "La fresa y la naca" — contenido perrero casual, divertido, con corazón
- **Popi:** pitbull mix, "la naca", energética, caótica, glotona 🐶
- **Luna:** shih tzu, "la fresita", diva, dramática, presumida 🌸
- **Tono:** mezcla CDMX + ternura, nada corporativo, mucho emoji

## Cuándo usar cada estilo de escena

| `estilo` | Cuándo usarlo |
|----------|---------------|
| `"intro"` | Primera escena, hook, título del reel |
| `"popi"` | Escenas de Popi / humor caótico / rojo |
| `"luna"` | Escenas de Luna / momentos fresa / rosa |
| `"default"` | Narración, datos, texto explicativo |
| `"outro"` | Llamada a la acción, despedida |

## Flujo de trabajo

1. **Entender el input:** la usuaria da un guion, una idea o un tema. Si es una idea vaga, genera tú el guion.
2. **Preguntar si tiene fotos:** si quiere usar fotos de Luna y Popi, pedirle que las suba (arrastre al chat en Claude Code desktop, o dé las rutas si ya están en el sistema).
3. **Diseñar las escenas:** 5-8 escenas de 2-4 s (total 15-30 s). Intercalar: 1 escena intro sin foto → 2-3 escenas con foto → 1 outro sin foto.
4. **Asignar fotos:** cada escena con foto lleva `"imagen": "/ruta/foto.jpg"`.
5. **Generar el JSON** y escribirlo en `/tmp/reel_config.json`.
6. **Ejecutar el script** con audio:
   ```bash
   python3 ~/.claude/skills/reels-animados/scripts/crear_reel.py /tmp/reel_config.json \
     -o ~/reel_output.mp4 --lofi
   # O con música propia:
   python3 ~/.claude/skills/reels-animados/scripts/crear_reel.py /tmp/reel_config.json \
     -o ~/reel_output.mp4 --audio /ruta/cancion.mp3 --volume 0.3
   ```
7. **Reportar** la ruta del MP4 y ofrecer ajustes.

### Cómo subir fotos al sistema

- **Claude Code desktop:** arrastra la foto al chat — Claude la recibe en una ruta temporal
- **Terminal:** `cp ~/Downloads/luna.jpg /tmp/luna.jpg` y luego pasar esa ruta en el JSON
- **Múltiples fotos:** recomendable meterlas en una carpeta: `/tmp/fotos_perritas/`

## Schema del JSON de configuración

```json
{
  "titulo": "Nombre del reel",
  "escenas": [
    {
      "imagen": "/ruta/absoluta/foto.jpg",
      "texto": "Texto principal corto",
      "subtitulo": "Texto secundario opcional más largo",
      "emoji": "🐾",
      "estilo": "intro",
      "duracion": 2.5
    }
  ]
}
```

**Campo `imagen` (opcional):** ruta absoluta a una foto JPG/PNG. Si se provee:
- La foto se usa como fondo completo de la escena (modo *cover*, recorte centrado)
- Se aplica un gradiente oscuro en la mitad inferior para que el texto sea legible
- El `emoji` se omite (ya hay foto de fondo)
- Si la ruta no existe, cae back a fondo de color automáticamente

**Escenas sin `imagen`:** fondo de color/gradiente según el `estilo`.

## Reglas de guionismo

- El `texto` de cada escena: **máximo 8 palabras**, todo caps o capitalizado
- El `subtitulo`: complementa, no repite. Puede ser más largo (15 palabras).
- Primera escena siempre = hook que engancha en 2 s
- Última escena siempre = CTA: "síguenos", "dale like", "etiqueta a tu fresa o naca"
- Mezcla escenas de Popi y Luna para crear contraste
- Usa emojis relevantes: 🐾🌸💅🍓🐶😂❤️

## Ejemplo completo

Input: *"reel del momento en que Popi se robó el taco de Luna"*

```json
{
  "titulo": "El taco robado",
  "escenas": [
    { "texto": "EL DRAMA DEL AÑO", "emoji": "😱", "estilo": "intro", "duracion": 2.5 },
    { "texto": "Luna tenía su taco", "emoji": "🌮🌸", "estilo": "luna", "duracion": 3.0 },
    { "texto": "Popi lo vio", "subtitulo": "Y tomó una decisión de vida", "emoji": "👀", "estilo": "popi", "duracion": 2.5 },
    { "texto": "ROBADO", "subtitulo": "En 0.3 segundos", "emoji": "💨🐶", "estilo": "popi", "duracion": 2.0 },
    { "texto": "Luna devastada", "emoji": "😭🌸", "estilo": "luna", "duracion": 3.0 },
    { "texto": "¿Cuál eres tú?", "subtitulo": "La fresa o la naca 👇", "emoji": "🍓🆚🎭", "estilo": "outro", "duracion": 3.5 }
  ]
}
```

## Audio — tres opciones integradas

El script maneja el audio directamente. Son mutuamente excluyentes:

### Opción 1: Archivo de música de fondo (recomendada)
```bash
python3 ~/.claude/skills/reels-animados/scripts/crear_reel.py config.json \
  -o reel.mp4 --audio /ruta/a/musica.mp3 --volume 0.25
```
- `--volume` va de 0.0 (silencio) a 1.0 (volumen completo). Default: 0.3
- Acepta MP3, WAV, AAC, OGG, M4A
- Si la música es más corta que el video, hace **loop automático**
- Si es más larga, la **recorta** automáticamente
- Aplica **fade in/out** de 0.5s al audio

### Opción 2: Beat lo-fi generado con ffmpeg (sin dependencias)
```bash
python3 ~/.claude/skills/reels-animados/scripts/crear_reel.py config.json \
  -o reel.mp4 --lofi
```
Genera un beat ambiental suave (capas de kick, bajo, hihat y tono ambiental) usando solo ffmpeg. No requiere instalar nada extra. Buen resultado para contenido casual/perrero.

### Opción 3: Voiceover TTS automático
```bash
pip install gtts   # una sola vez
python3 ~/.claude/skills/reels-animados/scripts/crear_reel.py config.json \
  -o reel.mp4 --tts
```
Lee en voz alta el `texto` y `subtitulo` de cada escena en español usando Google TTS.

### Sin audio (default)
Si no se pasa ninguna opción de audio, el video se genera sin pista de audio.

## Resolución de problemas

- **Error de fuente:** el script usa DejaVu/Liberation; si no están disponibles usa la fuente por defecto
- **Video muy pesado:** añadir `-crf 28` al comando ffmpeg reduce el tamaño
- **Texto cortado:** reducir el tamaño de fuente en el JSON o acortar el texto
