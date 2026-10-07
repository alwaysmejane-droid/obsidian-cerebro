---
name: otras-ias
description: Llama a modelos de IA gratuitos o de bajo costo de otros proveedores (Gemini, Groq, OpenRouter) y devuelve su respuesta. Úsala cuando la usuaria pida "pregúntale a Gemini", "prueba con Groq", "qué dice otro modelo sobre esto", "segunda opinión de otra IA", o quiera comparar respuestas entre modelos.
---

# Skill: otras-ias

Consulta modelos de otras IAs usando sus APIs gratuitas. Las claves van **siempre** en variables de entorno.

## Proveedores soportados

| Proveedor | Var de entorno | Modelos gratis / económicos |
|-----------|---------------|----------------------------|
| **Gemini** | `GEMINI_API_KEY` | `gemini-1.5-flash`, `gemini-1.5-flash-8b` |
| **Groq** | `GROQ_API_KEY` | `llama-3.1-8b-instant`, `llama3-70b-8192`, `mixtral-8x7b-32768` |
| **OpenRouter** | `OPENROUTER_API_KEY` | `meta-llama/llama-3.1-8b-instruct:free`, `mistralai/mistral-7b-instruct:free`, `google/gemma-2-9b-it:free` |

## Cómo usar el script

```bash
# Pregunta simple
python3 ~/.claude/skills/otras-ias/scripts/otras_ias.py \
  --provider gemini \
  --prompt "¿Cuál es la raza de perro más popular en México?"

# Con modelo específico
python3 ~/.claude/skills/otras-ias/scripts/otras_ias.py \
  --provider groq \
  --model llama3-70b-8192 \
  --prompt "Explica el concepto de overfitting en 2 oraciones"

# Comparar dos modelos
python3 ~/.claude/skills/otras-ias/scripts/otras_ias.py \
  --provider openrouter \
  --model "meta-llama/llama-3.1-8b-instruct:free" \
  --prompt "¿Qué es mejor para un perro: croquetas o BARF?"

# Con system prompt personalizado
python3 ~/.claude/skills/otras-ias/scripts/otras_ias.py \
  --provider gemini \
  --system "Eres un veterinario experto en razas pequeñas" \
  --prompt "¿Cuánto ejercicio necesita un shih tzu adulto?"
```

## Flujo de trabajo para la usuaria

1. **Verificar que la API key esté configurada** antes de llamar:
   ```bash
   echo $GEMINI_API_KEY | head -c 10
   ```
   Si no está configurada, instruir cómo agregarla (ver sección "Configurar API keys").

2. **Ejecutar el script** con el proveedor y prompt.

3. **Mostrar la respuesta** formateada, indicando claramente qué modelo respondió.

4. **Opcionalmente comparar**: ejecutar el mismo prompt en dos proveedores y mostrar las respuestas una al lado de la otra.

## Configurar API keys

Las keys van en el archivo de entorno de Claude Code o en el shell. **Nunca en el código.**

### Opción A: En Claude Code (persistente)
```bash
# Agregar a ~/.claude/settings.json bajo "env":
# { "env": { "GEMINI_API_KEY": "...", "GROQ_API_KEY": "...", "OPENROUTER_API_KEY": "..." } }
```
O usar: `/config` → Settings → Environment Variables

### Opción B: En el shell (sesión actual)
```bash
export GEMINI_API_KEY="tu_key_aqui"
export GROQ_API_KEY="tu_key_aqui"
export OPENROUTER_API_KEY="tu_key_aqui"
```

### Dónde obtener las keys (todas gratuitas):
- **Gemini:** https://aistudio.google.com/app/apikey
- **Groq:** https://console.groq.com/keys
- **OpenRouter:** https://openrouter.ai/keys (tier gratuito disponible)

## Cuándo recomendar cada proveedor

| Caso de uso | Recomendación |
|-------------|--------------|
| Respuesta rápida, larga | Gemini Flash (contexto 1M tokens) |
| Velocidad máxima | Groq (LLaMA en hardware especializado) |
| Variedad de modelos gratis | OpenRouter |
| Segunda opinión técnica | Groq llama3-70b |
| Tareas creativas | OpenRouter mistral-7b |

## Respuesta esperada del script

El script imprime:
```
=== Respuesta de gemini-1.5-flash ===
[respuesta del modelo]
=== Tokens usados: XXX ===
```

## Si la key no está configurada

```
❌ GEMINI_API_KEY no está configurada.
Obtén tu key gratis en: https://aistudio.google.com/app/apikey
Luego configúrala con:
  export GEMINI_API_KEY="tu_key"
O agrégala permanentemente en ~/.claude/settings.json
```
