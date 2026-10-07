---
name: apps-externas
description: Configura conectores MCP para conectar Claude con apps externas (Notion, Obsidian, bases de datos, Slack, GitHub, etc.) y permite pedir tareas desde esas apps. Úsala cuando la usuaria pida conectar una app, agregar un conector, "quiero pedirle tareas desde Notion", "conectar con mi base de datos", o configurar un servidor MCP nuevo.
---

# Skill: apps-externas

Configura y gestiona servidores MCP (Model Context Protocol) para que Claude pueda interactuar con apps externas.

## ¿Qué es un conector MCP?

MCP (Model Context Protocol) permite a Claude leer y escribir datos de apps externas directamente en la conversación. Una vez configurado, puedes decirle a Claude cosas como:
- "Busca en mi Notion las notas de las perritas"
- "Agrega esta tarea a mi lista de Obsidian"
- "Consulta mi base de datos de seguidores"

## Archivo de configuración

Los MCP servers van en `~/.claude/settings.json` bajo la clave `mcpServers`:

```json
{
  "mcpServers": {
    "nombre-servidor": {
      "command": "npx",
      "args": ["-y", "@paquete/servidor-mcp"],
      "env": {
        "API_KEY": "${NOMBRE_VAR_ENV}"
      }
    }
  }
}
```

**Regla clave:** las API keys siempre en variables de entorno (`${VAR}`), nunca en texto plano.

## Conectores más útiles y cómo instalarlos

### 1. Obsidian (notas y vault)

```bash
npm install -g obsidian-mcp
```

En `~/.claude/settings.json`:
```json
{
  "mcpServers": {
    "obsidian": {
      "command": "obsidian-mcp",
      "args": ["--vault", "/ruta/a/tu/vault"],
      "env": {}
    }
  }
}
```

**Capacidades:** leer notas, buscar en el vault, crear y editar notas.

---

### 2. Notion

```bash
npm install -g @notionhq/notion-mcp-server
```

```json
{
  "mcpServers": {
    "notion": {
      "command": "npx",
      "args": ["-y", "@notionhq/notion-mcp-server"],
      "env": {
        "OPENAPI_MCP_HEADERS": "{\"Authorization\": \"Bearer ${NOTION_API_KEY}\", \"Notion-Version\": \"2022-06-28\"}"
      }
    }
  }
}
```

Obtén tu integration key en: https://www.notion.so/my-integrations

---

### 3. Filesystem local (leer/escribir archivos)

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y", "@modelcontextprotocol/server-filesystem",
        "/ruta/permitida/1",
        "/ruta/permitida/2"
      ]
    }
  }
}
```

**Uso típico:** `/Users/tu_usuario/Documents`, `~/obsidian-vault`

---

### 4. GitHub

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

---

### 5. Base de datos SQLite

```json
{
  "mcpServers": {
    "sqlite": {
      "command": "uvx",
      "args": ["mcp-server-sqlite", "--db-path", "/ruta/a/tu/base.db"]
    }
  }
}
```

---

### 6. Slack

```json
{
  "mcpServers": {
    "slack": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-slack"],
      "env": {
        "SLACK_BOT_TOKEN": "${SLACK_BOT_TOKEN}",
        "SLACK_TEAM_ID": "${SLACK_TEAM_ID}"
      }
    }
  }
}
```

---

### 7. Google Drive (ya disponible en Claude.ai)

Si usas claude.ai, Google Drive ya está disponible como conector nativo. No necesita configuración MCP manual — actívalo en Settings → Connectors.

---

### 8. Servidor personalizado (Python simple)

Para apps caseras o APIs propias:

```python
# mi_servidor_mcp.py
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("mi-app")

@mcp.tool()
def obtener_dato(nombre: str) -> str:
    """Obtiene un dato de mi app"""
    return f"Dato de {nombre}"

if __name__ == "__main__":
    mcp.run()
```

```bash
pip install mcp
```

```json
{
  "mcpServers": {
    "mi-app": {
      "command": "python3",
      "args": ["/ruta/a/mi_servidor_mcp.py"]
    }
  }
}
```

## Cómo agregar un nuevo conector

### Proceso paso a paso:

1. **Leer `~/.claude/settings.json`** actual
2. **Agregar el nuevo servidor** bajo `mcpServers`
3. **Configurar las variables de entorno** necesarias
4. **Guardar el archivo**
5. **Reiniciar Claude Code** (o usar `/mcp restart` si está disponible)
6. **Verificar** que el servidor aparece activo

### Verificar conectores activos:
```bash
# Ver settings actuales
cat ~/.claude/settings.json | python3 -m json.tool

# Verificar que una variable de entorno está configurada
echo ${NOMBRE_VAR} | head -c 8
```

## Conectores ya disponibles en esta sesión

Los siguientes conectores ya están activos (sin configuración adicional):
- **Google Drive** — leer, buscar, crear archivos
- **Gmail** — leer y enviar correos
- **Google Calendar** — ver y crear eventos
- **GitHub** — ver repos, PRs, issues

## Solución de problemas comunes

| Error | Causa | Solución |
|-------|-------|---------|
| `MCP endpoint not found` | URL incorrecta del servidor | Verificar la URL/ruta en settings.json |
| `requires authentication` | Falta la API key | Configurar la variable de entorno |
| Servidor no aparece | settings.json mal formado | Validar JSON con `python3 -m json.tool` |
| `npx: command not found` | Node.js no instalado | Instalar Node.js o usar `uvx` para servidores Python |

## Ejemplo completo: conectar Obsidian + Notion

```json
{
  "mcpServers": {
    "obsidian": {
      "command": "obsidian-mcp",
      "args": ["--vault", "~/Documents/MiVault"]
    },
    "notion": {
      "command": "npx",
      "args": ["-y", "@notionhq/notion-mcp-server"],
      "env": {
        "OPENAPI_MCP_HEADERS": "{\"Authorization\": \"Bearer ${NOTION_API_KEY}\", \"Notion-Version\": \"2022-06-28\"}"
      }
    }
  },
  "env": {
    "NOTION_API_KEY": "tu_key_aqui"
  }
}
```

Después de guardar: reinicia Claude Code y ya puedes decir "busca en mi Notion las notas sobre Popi y Luna".
