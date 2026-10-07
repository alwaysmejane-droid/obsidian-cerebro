#!/usr/bin/env python3
"""
otras_ias.py — Consulta modelos de Gemini, Groq y OpenRouter
Las API keys se leen SIEMPRE de variables de entorno. Nunca en el código.

Uso:
  python3 otras_ias.py --provider gemini --prompt "tu pregunta"
  python3 otras_ias.py --provider groq --model llama3-70b-8192 --prompt "..."
  python3 otras_ias.py --provider openrouter --prompt "..." --system "Eres..."
"""
import argparse
import json
import os
import sys
import urllib.request
import urllib.error

DEFAULTS = {
    "gemini":     "gemini-1.5-flash",
    "groq":       "llama-3.1-8b-instant",
    "openrouter": "meta-llama/llama-3.1-8b-instruct:free",
}


def err(msg):
    print(f"❌ {msg}", file=sys.stderr)
    sys.exit(1)


def http_post(url, headers, body):
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace")
        err(f"HTTP {e.code}: {raw[:400]}")
    except urllib.error.URLError as e:
        err(f"Red: {e.reason}")


def call_gemini(prompt, model, system=None):
    key = os.environ.get("GEMINI_API_KEY", "")
    if not key:
        err("GEMINI_API_KEY no está configurada.\n"
            "Obtén tu key gratis en: https://aistudio.google.com/app/apikey\n"
            "Configúrala con: export GEMINI_API_KEY=\"tu_key\"")

    url = (f"https://generativelanguage.googleapis.com/v1beta/models/"
           f"{model}:generateContent?key={key}")
    contents = []
    if system:
        contents.append({"role": "user", "parts": [{"text": f"[INSTRUCCIONES]: {system}"}]})
        contents.append({"role": "model", "parts": [{"text": "Entendido."}]})
    contents.append({"role": "user", "parts": [{"text": prompt}]})

    body = {"contents": contents,
            "generationConfig": {"temperature": 0.7, "maxOutputTokens": 2048}}
    resp = http_post(url, {"Content-Type": "application/json"}, body)

    text = resp["candidates"][0]["content"]["parts"][0]["text"]
    tokens = resp.get("usageMetadata", {})
    used = tokens.get("totalTokenCount", "?")
    return text, model, used


def call_groq(prompt, model, system=None):
    key = os.environ.get("GROQ_API_KEY", "")
    if not key:
        err("GROQ_API_KEY no está configurada.\n"
            "Obtén tu key gratis en: https://console.groq.com/keys\n"
            "Configúrala con: export GROQ_API_KEY=\"tu_key\"")

    url = "https://api.groq.com/openai/v1/chat/completions"
    msgs = []
    if system:
        msgs.append({"role": "system", "content": system})
    msgs.append({"role": "user", "content": prompt})

    body = {"model": model, "messages": msgs,
            "temperature": 0.7, "max_tokens": 2048}
    resp = http_post(url,
                     {"Content-Type": "application/json",
                      "Authorization": f"Bearer {key}"},
                     body)

    text = resp["choices"][0]["message"]["content"]
    used = resp.get("usage", {}).get("total_tokens", "?")
    return text, resp["model"], used


def call_openrouter(prompt, model, system=None):
    key = os.environ.get("OPENROUTER_API_KEY", "")
    if not key:
        err("OPENROUTER_API_KEY no está configurada.\n"
            "Obtén tu key gratis en: https://openrouter.ai/keys\n"
            "Configúrala con: export OPENROUTER_API_KEY=\"tu_key\"")

    url = "https://openrouter.ai/api/v1/chat/completions"
    msgs = []
    if system:
        msgs.append({"role": "system", "content": system})
    msgs.append({"role": "user", "content": prompt})

    body = {"model": model, "messages": msgs,
            "temperature": 0.7, "max_tokens": 2048}
    resp = http_post(url,
                     {"Content-Type": "application/json",
                      "Authorization": f"Bearer {key}",
                      "HTTP-Referer": "https://claude.ai",
                      "X-Title": "otras-ias-skill"},
                     body)

    text = resp["choices"][0]["message"]["content"]
    used = resp.get("usage", {}).get("total_tokens", "?")
    return text, resp.get("model", model), used


PROVIDERS = {
    "gemini":     call_gemini,
    "groq":       call_groq,
    "openrouter": call_openrouter,
}


def main():
    parser = argparse.ArgumentParser(
        description="Consulta modelos de otras IAs (Gemini, Groq, OpenRouter)"
    )
    parser.add_argument("--provider", "-p",
                        choices=list(PROVIDERS), required=True,
                        help="Proveedor: gemini | groq | openrouter")
    parser.add_argument("--model", "-m", default=None,
                        help="Modelo específico (por defecto usa el recomendado del proveedor)")
    parser.add_argument("--prompt", required=True,
                        help="Prompt / pregunta a enviar")
    parser.add_argument("--system", "-s", default=None,
                        help="System prompt opcional")
    args = parser.parse_args()

    model = args.model or DEFAULTS[args.provider]
    fn = PROVIDERS[args.provider]

    print(f"\n⏳ Consultando {args.provider} ({model})...\n")
    text, actual_model, tokens = fn(args.prompt, model, args.system)

    print(f"=== Respuesta de {actual_model} ===")
    print(text)
    print(f"\n=== Tokens usados: {tokens} ===\n")


if __name__ == "__main__":
    main()
