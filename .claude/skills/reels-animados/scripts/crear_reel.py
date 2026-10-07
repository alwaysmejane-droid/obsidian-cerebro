#!/usr/bin/env python3
"""
crear_reel.py — Genera reels verticales 9:16 para "La fresa y la naca"

Uso:
  python3 crear_reel.py config.json -o output.mp4
  python3 crear_reel.py config.json -o output.mp4 --audio musica.mp3
  python3 crear_reel.py config.json -o output.mp4 --audio musica.mp3 --volume 0.25
  python3 crear_reel.py config.json -o output.mp4 --tts  # (requiere gtts: pip install gtts)
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile
from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT, FPS = 1080, 1920, 30

PALETA = {
    "fondo":    (20, 15, 30),
    "fondo2":   (35, 25, 50),
    "popi1":    (40, 12, 12),
    "popi2":    (70, 22, 22),
    "popi_acc": (210, 70, 70),
    "luna1":    (22, 12, 30),
    "luna2":    (45, 18, 55),
    "luna_acc": (230, 100, 170),
    "intro1":   (10, 8, 20),
    "intro2":   (30, 20, 50),
    "acento":   (255, 200, 60),
    "texto":    (255, 255, 255),
    "subtexto": (200, 190, 210),
}

FONT_PATHS_BOLD = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",
]
FONT_PATHS_REGULAR = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
]


def get_font(size, bold=False):
    for fp in (FONT_PATHS_BOLD if bold else FONT_PATHS_REGULAR):
        if os.path.exists(fp):
            try:
                return ImageFont.truetype(fp, size)
            except Exception:
                continue
    return ImageFont.load_default()


def draw_gradient_bg(draw, c1, c2):
    for y in range(HEIGHT):
        t = y / HEIGHT
        r = int(c1[0] * (1 - t) + c2[0] * t)
        g = int(c1[1] * (1 - t) + c2[1] * t)
        b = int(c1[2] * (1 - t) + c2[2] * t)
        draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))


def wrap_text(text, font, max_w, draw):
    words = text.split()
    lines, current = [], ""
    for word in words:
        test = (current + " " + word).strip()
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] <= max_w:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines if lines else [""]


def render_scene(scene, alpha=1.0):
    img = Image.new("RGB", (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(img)
    style = scene.get("estilo", "default")

    if style == "popi":
        bg1, bg2, acc = PALETA["popi1"], PALETA["popi2"], PALETA["popi_acc"]
    elif style == "luna":
        bg1, bg2, acc = PALETA["luna1"], PALETA["luna2"], PALETA["luna_acc"]
    elif style in ("intro", "outro"):
        bg1, bg2, acc = PALETA["intro1"], PALETA["intro2"], PALETA["acento"]
    else:
        bg1, bg2, acc = PALETA["fondo"], PALETA["fondo2"], PALETA["acento"]

    draw_gradient_bg(draw, bg1, bg2)
    draw.rectangle([(0, 0), (WIDTH, 14)], fill=acc)
    draw.rectangle([(0, HEIGHT - 14), (WIDTH, HEIGHT)], fill=acc)
    draw.rectangle([(0, 0), (8, HEIGHT)], fill=acc)
    draw.rectangle([(WIDTH - 8, 0), (WIDTH, HEIGHT)], fill=acc)

    pad, max_w = 90, WIDTH - 180
    center_y = HEIGHT // 2
    offset_y = 0

    emoji = scene.get("emoji", "")
    if emoji:
        efont = get_font(110)
        try:
            draw.text((WIDTH // 2, center_y - 220), emoji,
                      font=efont, fill=PALETA["texto"], anchor="mm")
            offset_y = 120
        except Exception:
            pass

    main_text = scene.get("texto", "")
    if main_text:
        tfont = get_font(76, bold=True)
        lines = wrap_text(main_text, tfont, max_w, draw)
        line_h = 95
        total_h = len(lines) * line_h
        base_y = center_y - total_h // 2 + offset_y
        for i, line in enumerate(lines):
            y = base_y + i * line_h
            draw.text((WIDTH // 2 + 4, y + 4), line,
                      font=tfont, fill=(0, 0, 0), anchor="mm")
            draw.text((WIDTH // 2, y), line,
                      font=tfont, fill=PALETA["texto"], anchor="mm")
        offset_y += total_h // 2 + 40

    sub = scene.get("subtitulo", "")
    if sub:
        sfont = get_font(46)
        sub_lines = wrap_text(sub, sfont, max_w, draw)
        sub_y = center_y + offset_y + 20
        for i, line in enumerate(sub_lines):
            draw.text((WIDTH // 2, sub_y + i * 58), line,
                      font=sfont, fill=PALETA["subtexto"], anchor="mm")

    tagfont = get_font(38)
    draw.text((WIDTH // 2, HEIGHT - 85), "🐾 La fresa y la naca",
              font=tagfont, fill=acc, anchor="mm")

    if alpha < 0.999:
        black = Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 0))
        img = Image.blend(black, img, min(max(alpha, 0.0), 1.0))

    return img


# ── Audio helpers ─────────────────────────────────────────────────────────────

def generate_tts_audio(scenes, tmpdir):
    """Genera voiceover con gTTS si está instalado, devuelve ruta MP3 o None."""
    try:
        from gtts import gTTS
    except ImportError:
        print("⚠️  gTTS no instalado. Instalar con: pip install gtts", file=sys.stderr)
        return None

    full_text = " ".join(
        s.get("texto", "") + ". " + s.get("subtitulo", "")
        for s in scenes
        if s.get("texto") or s.get("subtitulo")
    )
    tts = gTTS(full_text, lang="es")
    tts_path = os.path.join(tmpdir, "voiceover.mp3")
    tts.save(tts_path)
    return tts_path


def mix_audio_with_video(video_path, audio_path, output_path, volume=0.3, total_duration=None):
    """
    Mezcla audio con video. El audio se hace loop si es más corto que el video,
    se recorta si es más largo, con fade in/out de 0.5 s.
    """
    fade_d = min(0.5, (total_duration or 3) * 0.1)

    filter_str = (
        f"[1:a]volume={volume},"
        f"afade=t=in:st=0:d={fade_d},"
        f"afade=t=out:st={max(0, (total_duration or 10) - fade_d)}:d={fade_d}"
        f"[audio_mixed]"
    )

    cmd = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-stream_loop", "-1",   # loop audio infinitely, luego -shortest lo recorta
        "-i", audio_path,
        "-filter_complex", filter_str,
        "-map", "0:v",
        "-map", "[audio_mixed]",
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "128k",
        "-shortest",
        output_path,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"⚠️  Error mezclando audio:\n{result.stderr[-500:]}", file=sys.stderr)
        return False
    return True


def generate_lofi_beat(tmpdir, duration):
    """
    Genera un beat lo-fi suave con ffmpeg puro (sin dependencias externas).
    Usa capas de senos con frecuencias armónicas para imitar un beat ambiental.
    """
    out = os.path.join(tmpdir, "lofi_beat.mp3")
    # Capas: kick suave (80Hz), bajo (120Hz), hihat (8kHz amortiguado), ambiente (440Hz)
    expr = (
        "0.3*sin(2*PI*80*t)*exp(-8*(t-floor(t*2)/2))+"   # kick cada 0.5s
        "0.2*sin(2*PI*120*t)*exp(-4*(t-floor(t*4)/4))+"   # bajo cada 0.25s
        "0.05*sin(2*PI*8000*t)*exp(-30*(t-floor(t*8)/8))+" # hihat sutil
        "0.08*sin(2*PI*440*(1+0.001*sin(2*PI*0.1*t))*t)"   # tono ambiental vibrato
    )
    cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi",
        "-i", f"aevalsrc='{expr}':s=44100:c=stereo",
        "-t", str(duration + 1),
        "-c:a", "libmp3lame", "-b:a", "96k",
        out,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"⚠️  No se pudo generar beat: {result.stderr[-200:]}", file=sys.stderr)
        return None
    return out


# ── Core ───────────────────────────────────────────────────────────────────────

def render_video_silent(scenes, tmpdir):
    """Renderiza el video sin audio, devuelve ruta del MP4."""
    fade_f = int(FPS * 0.25)
    list_file = os.path.join(tmpdir, "frames.txt")
    frame_idx = 0

    with open(list_file, "w") as lf:
        for scene in scenes:
            duration = float(scene.get("duracion", 3.0))
            total_f = max(int(duration * FPS), 1)
            for fi in range(total_f):
                if fi < fade_f:
                    alpha = fi / max(fade_f, 1)
                elif fi >= total_f - fade_f:
                    alpha = (total_f - fi) / max(fade_f, 1)
                else:
                    alpha = 1.0
                img = render_scene(scene, alpha=alpha)
                fp = os.path.join(tmpdir, f"f{frame_idx:07d}.png")
                img.save(fp, "PNG")
                lf.write(f"file '{fp}'\n")
                lf.write(f"duration {1/FPS:.6f}\n")
                frame_idx += 1

    silent_mp4 = os.path.join(tmpdir, "silent.mp4")
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", list_file,
        "-vf", f"scale={WIDTH}:{HEIGHT}:force_original_aspect_ratio=disable",
        "-c:v", "libx264", "-preset", "fast", "-crf", "23",
        "-pix_fmt", "yuv420p", "-r", str(FPS),
        silent_mp4,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error ffmpeg:\n{result.stderr}", file=sys.stderr)
        sys.exit(1)
    return silent_mp4


def create_reel(config_path, output_path, audio_path=None, volume=0.3,
                use_tts=False, use_lofi=False):
    with open(config_path, encoding="utf-8") as f:
        config = json.load(f)

    scenes = config.get("escenas", [])
    if not scenes:
        print("Error: el JSON no tiene 'escenas'", file=sys.stderr)
        sys.exit(1)

    total_dur = sum(float(s.get("duracion", 3)) for s in scenes)

    with tempfile.TemporaryDirectory() as tmpdir:
        # 1. Renderizar video silencioso
        silent_mp4 = render_video_silent(scenes, tmpdir)

        # 2. Resolver fuente de audio
        final_audio = audio_path

        if use_tts and not final_audio:
            print("🎙️  Generando voiceover TTS...")
            final_audio = generate_tts_audio(scenes, tmpdir)

        if use_lofi and not final_audio:
            print("🎵 Generando beat lo-fi con ffmpeg...")
            final_audio = generate_lofi_beat(tmpdir, total_dur)

        # 3. Mezclar o copiar
        audio_mixed = False
        if final_audio and os.path.exists(final_audio):
            print(f"🔊 Mezclando audio (vol={volume})...")
            audio_mixed = mix_audio_with_video(silent_mp4, final_audio, output_path,
                                               volume=volume, total_duration=total_dur)
            if not audio_mixed:
                print("⚠️  Falló la mezcla, guardando sin audio...", file=sys.stderr)

        if not audio_mixed:
            import shutil
            shutil.copy(silent_mp4, output_path)
            if final_audio and not os.path.exists(final_audio):
                print(f"⚠️  Audio no encontrado: {final_audio}", file=sys.stderr)

    size_mb = os.path.getsize(output_path) / 1024 / 1024
    audio_tag = "🔊 con audio" if audio_mixed else "🔇 sin audio"
    print(f"\n✅ Reel listo: {output_path}")
    print(f"   Duración: {total_dur:.1f}s | Escenas: {len(scenes)} | {audio_tag} | Tamaño: {size_mb:.1f} MB")


def main():
    parser = argparse.ArgumentParser(
        description="Genera reels verticales 9:16 para La fresa y la naca"
    )
    parser.add_argument("config", help="JSON de configuración con escenas")
    parser.add_argument("-o", "--output", default="reel.mp4", help="MP4 de salida")

    audio_group = parser.add_mutually_exclusive_group()
    audio_group.add_argument("--audio", metavar="ARCHIVO",
                             help="Archivo de audio (MP3, WAV, AAC, etc.) como música de fondo")
    audio_group.add_argument("--tts", action="store_true",
                             help="Genera voiceover automático con gTTS (requiere: pip install gtts)")
    audio_group.add_argument("--lofi", action="store_true",
                             help="Genera beat lo-fi ambiental con ffmpeg (sin dependencias extra)")

    parser.add_argument("--volume", type=float, default=0.3,
                        help="Volumen del audio de fondo (0.0-1.0, default: 0.3)")
    args = parser.parse_args()

    create_reel(
        args.config, args.output,
        audio_path=args.audio,
        volume=args.volume,
        use_tts=args.tts,
        use_lofi=args.lofi,
    )


if __name__ == "__main__":
    main()
