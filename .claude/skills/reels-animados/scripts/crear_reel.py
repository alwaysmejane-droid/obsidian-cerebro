#!/usr/bin/env python3
"""
crear_reel.py — Genera reels verticales 9:16 para "La fresa y la naca"

Uso:
  python3 crear_reel.py config.json -o output.mp4
  python3 crear_reel.py config.json -o output.mp4 --lofi
  python3 crear_reel.py config.json -o output.mp4 --audio musica.mp3 --volume 0.25
  python3 crear_reel.py config.json -o output.mp4 --tts   # pip install gtts

Escenas con foto:
  { "imagen": "/ruta/foto.jpg", "texto": "Mi perra", "estilo": "luna" }
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

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


# ── Foto helpers ───────────────────────────────────────────────────────────────

def load_photo_as_bg(photo_path, style):
    """
    Carga una foto y la convierte en fondo 9:16.
    - Recorta al centro para cubrir todo el frame (cover)
    - Ajusta brillo/saturación según el estilo
    - Devuelve imagen PIL RGB de WIDTH x HEIGHT
    """
    try:
        photo = Image.open(photo_path).convert("RGB")
    except Exception as e:
        print(f"⚠️  No pude abrir {photo_path}: {e}", file=sys.stderr)
        return None

    # Escalar para cubrir 9:16 (cover, no distorsionar)
    ph, pw = photo.height, photo.width
    target_ratio = HEIGHT / WIDTH  # 1920/1080 = 1.777...
    photo_ratio = ph / pw

    if photo_ratio > target_ratio:
        # foto más alta que 9:16 → ajustar por ancho
        new_w = WIDTH
        new_h = int(pw * target_ratio * (WIDTH / pw))
        # Reescalar manteniendo proporción desde el ancho
        new_h = int(ph * (WIDTH / pw))
        photo = photo.resize((WIDTH, new_h), Image.LANCZOS)
        # Crop vertical centrado
        top = (new_h - HEIGHT) // 2
        photo = photo.crop((0, top, WIDTH, top + HEIGHT))
    else:
        # foto más ancha que 9:16 → ajustar por alto
        new_h = HEIGHT
        new_w = int(pw * (HEIGHT / ph))
        photo = photo.resize((new_w, HEIGHT), Image.LANCZOS)
        # Crop horizontal centrado
        left = (new_w - WIDTH) // 2
        photo = photo.crop((left, 0, left + WIDTH, HEIGHT))

    # Ajuste de color según estilo
    if style == "popi":
        # Tono cálido rojizo sutil
        photo = ImageEnhance.Color(photo).enhance(1.2)
        photo = ImageEnhance.Brightness(photo).enhance(0.85)
    elif style == "luna":
        # Tono suave rosado
        photo = ImageEnhance.Color(photo).enhance(1.1)
        photo = ImageEnhance.Brightness(photo).enhance(0.9)
    else:
        photo = ImageEnhance.Brightness(photo).enhance(0.8)

    return photo


def add_photo_overlays(img, style):
    """
    Agrega gradiente oscuro en la mitad inferior para legibilidad del texto,
    y barra de color en top/bottom según estilo.
    """
    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # Gradiente negro en la franja inferior (texto)
    grad_start = int(HEIGHT * 0.45)
    for y in range(grad_start, HEIGHT):
        t = (y - grad_start) / (HEIGHT - grad_start)
        alpha = int(180 * t)  # 0 → 180 (muy opaco al fondo)
        draw.line([(0, y), (WIDTH, y)], fill=(0, 0, 0, alpha))

    # Gradiente sutil en franja superior
    for y in range(0, int(HEIGHT * 0.25)):
        t = 1 - (y / (HEIGHT * 0.25))
        alpha = int(100 * t)
        draw.line([(0, y), (WIDTH, y)], fill=(0, 0, 0, alpha))

    img_rgba = img.convert("RGBA")
    img_rgba = Image.alpha_composite(img_rgba, overlay)
    return img_rgba.convert("RGB")


# ── Scene renderer ─────────────────────────────────────────────────────────────

def render_scene(scene, alpha=1.0):
    style = scene.get("estilo", "default")
    photo_path = scene.get("imagen", "")

    if style == "popi":
        acc = PALETA["popi_acc"]
    elif style == "luna":
        acc = PALETA["luna_acc"]
    elif style in ("intro", "outro"):
        acc = PALETA["acento"]
    else:
        acc = PALETA["acento"]

    # ── Fondo: foto o gradiente ────────────────────────────────────────────
    if photo_path and os.path.exists(photo_path):
        bg = load_photo_as_bg(photo_path, style)
        if bg is None:
            photo_path = ""  # fallback a gradiente

    if not photo_path or not os.path.exists(photo_path):
        bg = Image.new("RGB", (WIDTH, HEIGHT))
        draw_bg = ImageDraw.Draw(bg)
        if style == "popi":
            draw_gradient_bg(draw_bg, PALETA["popi1"], PALETA["popi2"])
        elif style == "luna":
            draw_gradient_bg(draw_bg, PALETA["luna1"], PALETA["luna2"])
        elif style in ("intro", "outro"):
            draw_gradient_bg(draw_bg, PALETA["intro1"], PALETA["intro2"])
        else:
            draw_gradient_bg(draw_bg, PALETA["fondo"], PALETA["fondo2"])
    else:
        bg = add_photo_overlays(bg, style)

    img = bg.copy()
    draw = ImageDraw.Draw(img)

    # ── Barras de color (top/bottom) ───────────────────────────────────────
    draw.rectangle([(0, 0), (WIDTH, 10)], fill=acc)
    draw.rectangle([(0, HEIGHT - 10), (WIDTH, HEIGHT)], fill=acc)
    draw.rectangle([(0, 0), (6, HEIGHT)], fill=acc)
    draw.rectangle([(WIDTH - 6, 0), (WIDTH, HEIGHT)], fill=acc)

    # ── Texto principal (zona inferior sobre gradiente oscuro) ─────────────
    pad, max_w = 80, WIDTH - 160

    main_text = scene.get("texto", "")
    text_bottom_y = HEIGHT - 200  # ancla: texto principal termina aquí

    if main_text:
        tfont = get_font(74, bold=True)
        lines = wrap_text(main_text, tfont, max_w, draw)
        line_h = 92
        total_h = len(lines) * line_h
        base_y = text_bottom_y - total_h

        for i, line in enumerate(lines):
            y = base_y + i * line_h
            # Sombra difusa
            for dx, dy in [(-3, -3), (3, -3), (-3, 3), (3, 3), (0, 4)]:
                draw.text((WIDTH // 2 + dx, y + dy), line,
                          font=tfont, fill=(0, 0, 0, 200), anchor="mm")
            draw.text((WIDTH // 2, y), line,
                      font=tfont, fill=PALETA["texto"], anchor="mm")

    # ── Subtítulo ──────────────────────────────────────────────────────────
    sub = scene.get("subtitulo", "")
    if sub:
        sfont = get_font(44)
        sub_lines = wrap_text(sub, sfont, max_w, draw)
        sub_y = text_bottom_y + 20
        for i, line in enumerate(sub_lines):
            draw.text((WIDTH // 2 + 2, sub_y + i * 55 + 2), line,
                      font=sfont, fill=(0, 0, 0), anchor="mm")
            draw.text((WIDTH // 2, sub_y + i * 55), line,
                      font=sfont, fill=PALETA["subtexto"], anchor="mm")

    # ── Emoji (en escenas sin foto, centrado arriba) ───────────────────────
    emoji = scene.get("emoji", "")
    if emoji and not (photo_path and os.path.exists(photo_path)):
        efont = get_font(110)
        try:
            draw.text((WIDTH // 2, HEIGHT // 2 - 150), emoji,
                      font=efont, fill=PALETA["texto"], anchor="mm")
        except Exception:
            pass

    # ── Watermark canal ────────────────────────────────────────────────────
    tagfont = get_font(36)
    # Caja semitransparente detrás del watermark
    wm_text = "🐾 La fresa y la naca"
    wm_y = HEIGHT - 72
    try:
        bbox = draw.textbbox((WIDTH // 2, wm_y), wm_text, font=tagfont, anchor="mm")
        draw.rectangle(
            [bbox[0] - 14, bbox[1] - 6, bbox[2] + 14, bbox[3] + 6],
            fill=(0, 0, 0, 140)
        )
    except Exception:
        pass
    draw.text((WIDTH // 2, wm_y), wm_text, font=tagfont, fill=acc, anchor="mm")

    # ── Fade in/out ────────────────────────────────────────────────────────
    if alpha < 0.999:
        black = Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 0))
        img = Image.blend(black, img, min(max(alpha, 0.0), 1.0))

    return img


# ── Audio helpers ──────────────────────────────────────────────────────────────

def generate_tts_audio(scenes, tmpdir):
    try:
        from gtts import gTTS
    except ImportError:
        print("⚠️  gTTS no instalado. Instalar con: pip install gtts", file=sys.stderr)
        return None
    full_text = " ".join(
        s.get("texto", "") + ". " + s.get("subtitulo", "")
        for s in scenes if s.get("texto") or s.get("subtitulo")
    )
    tts = gTTS(full_text, lang="es")
    path = os.path.join(tmpdir, "voiceover.mp3")
    tts.save(path)
    return path


def generate_lofi_beat(tmpdir, duration):
    out = os.path.join(tmpdir, "lofi_beat.mp3")
    expr = (
        "0.3*sin(2*PI*80*t)*exp(-8*(t-floor(t*2)/2))+"
        "0.2*sin(2*PI*120*t)*exp(-4*(t-floor(t*4)/4))+"
        "0.05*sin(2*PI*8000*t)*exp(-30*(t-floor(t*8)/8))+"
        "0.08*sin(2*PI*440*(1+0.001*sin(2*PI*0.1*t))*t)"
    )
    cmd = [
        "ffmpeg", "-y", "-f", "lavfi",
        "-i", f"aevalsrc='{expr}':s=44100:c=stereo",
        "-t", str(duration + 1),
        "-c:a", "libmp3lame", "-b:a", "96k", out,
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"⚠️  No se pudo generar beat: {r.stderr[-200:]}", file=sys.stderr)
        return None
    return out


def mix_audio_with_video(video_path, audio_path, output_path, volume=0.3, total_duration=None):
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
        "-stream_loop", "-1",
        "-i", audio_path,
        "-filter_complex", filter_str,
        "-map", "0:v", "-map", "[audio_mixed]",
        "-c:v", "copy", "-c:a", "aac", "-b:a", "128k",
        "-shortest", output_path,
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"⚠️  Error mezclando audio:\n{r.stderr[-500:]}", file=sys.stderr)
        return False
    return True


# ── Core ───────────────────────────────────────────────────────────────────────

def render_video_silent(scenes, tmpdir):
    fade_f = int(FPS * 0.25)
    list_file = os.path.join(tmpdir, "frames.txt")
    frame_idx = 0

    # Pre-cache: render one base frame per scene (alpha=1.0) to avoid
    # re-processing photos and gradients on every frame.
    scene_bases = []
    black = Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 0))
    for scene in scenes:
        base = render_scene(scene, alpha=1.0)
        scene_bases.append(base)

    with open(list_file, "w") as lf:
        for scene, base in zip(scenes, scene_bases):
            duration = float(scene.get("duracion", 3.0))
            total_f = max(int(duration * FPS), 1)
            for fi in range(total_f):
                if fi < fade_f:
                    alpha = fi / max(fade_f, 1)
                elif fi >= total_f - fade_f:
                    alpha = (total_f - fi) / max(fade_f, 1)
                else:
                    alpha = 1.0

                if alpha < 0.999:
                    img = Image.blend(black, base, min(max(alpha, 0.0), 1.0))
                else:
                    img = base

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
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"Error ffmpeg:\n{r.stderr}", file=sys.stderr)
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
    foto_count = sum(1 for s in scenes if s.get("imagen") and os.path.exists(s["imagen"]))
    if foto_count:
        print(f"📸 {foto_count} foto(s) encontrada(s)")

    with tempfile.TemporaryDirectory() as tmpdir:
        silent_mp4 = render_video_silent(scenes, tmpdir)

        final_audio = audio_path
        if use_tts and not final_audio:
            print("🎙️  Generando voiceover TTS...")
            final_audio = generate_tts_audio(scenes, tmpdir)
        if use_lofi and not final_audio:
            print("🎵 Generando beat lo-fi...")
            final_audio = generate_lofi_beat(tmpdir, total_dur)

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

    size_mb = os.path.getsize(output_path) / 1024 / 1024
    audio_tag = "🔊 con audio" if audio_mixed else "🔇 sin audio"
    print(f"\n✅ Reel listo: {output_path}")
    print(f"   Duración: {total_dur:.1f}s | Escenas: {len(scenes)} | 📸 {foto_count} fotos | {audio_tag} | {size_mb:.1f} MB")


def main():
    parser = argparse.ArgumentParser(
        description="Genera reels verticales 9:16 para La fresa y la naca"
    )
    parser.add_argument("config", help="JSON con escenas")
    parser.add_argument("-o", "--output", default="reel.mp4")

    ag = parser.add_mutually_exclusive_group()
    ag.add_argument("--audio", metavar="ARCHIVO",
                    help="Archivo de música (MP3, WAV, AAC) como fondo")
    ag.add_argument("--tts", action="store_true",
                    help="Voiceover automático (requiere: pip install gtts)")
    ag.add_argument("--lofi", action="store_true",
                    help="Beat lo-fi generado con ffmpeg (sin dependencias)")

    parser.add_argument("--volume", type=float, default=0.3,
                        help="Volumen 0.0–1.0 (default 0.3)")
    args = parser.parse_args()
    create_reel(args.config, args.output,
                audio_path=args.audio, volume=args.volume,
                use_tts=args.tts, use_lofi=args.lofi)


if __name__ == "__main__":
    main()
