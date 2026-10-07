---
name: comandos-viz
description: Interpreta comandos cortos o frases naturales para generar visualizaciones interactivas como HTML Artifact. Úsala cuando la usuaria escriba comandos tipo "viz bar ventas", "muéstrame las visitas por día", "grafica los seguidores", "chart pie razas" o cualquier petición de gráfico con datos inline o pegados. Soporta barras, líneas, pastel/donut, dispersión, área e histograma.
---

# Skill: comandos-viz

Convierte comandos cortos o lenguaje natural en gráficos HTML interactivos (Chart.js) publicados como Artifact.

## Gramática de comandos cortos

```
viz <tipo> <descripción de datos>
chart <tipo> <descripción de datos>
grafica <tipo> <descripción de datos>
```

**Tipos soportados:**

| Alias aceptados | Tipo de gráfico |
|-----------------|----------------|
| `bar`, `barras`, `columnas` | Barras verticales |
| `barh`, `horizontal` | Barras horizontales |
| `line`, `línea`, `lineas`, `tendencia` | Líneas / serie temporal |
| `pie`, `pastel`, `dona`, `donut` | Pastel o donut |
| `scatter`, `dispersión`, `puntos` | Dispersión XY |
| `area` | Área apilada |
| `hist`, `histograma` | Histograma |

**Ejemplos de comandos:**
```
viz bar ventas por mes
viz line seguidores últimas 4 semanas
viz pie distribución razas de mis perritas
grafica barh top 5 posts por alcance
chart scatter peso vs energía
```

## También acepta lenguaje natural

Cualquiera de estas frases activa la skill:
- "muéstrame las ventas del mes en barras"
- "quiero ver la evolución de seguidores"
- "haz una gráfica de las razas más populares en México"
- "compara las visitas de enero vs febrero"

## Proceso de generación

### Paso 1: Parsear el comando

Extrae del comando o frase:
- **tipo_grafico**: uno de los tipos de la tabla
- **titulo**: descripción humanizada (ej: "Ventas por mes")
- **datos**: los datos a graficar (pueden estar en el comando, pegados después, o inventados como ejemplo)
- **eje_x**: etiqueta del eje X
- **eje_y**: etiqueta del eje Y (si aplica)

### Paso 2: Obtener los datos

Prioridad:
1. Si la usuaria pegó datos (tabla, CSV, lista) → úsalos directamente
2. Si mencionó datos con números en el comando → extráelos
3. Si no hay datos → genera datos de ejemplo realistas y avisa: "Usé datos de ejemplo — pégame los tuyos para actualizarlos"

### Paso 3: Generar el Artifact HTML

Usa Chart.js desde CDN. El template base:

```html
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{{TITULO}}</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4/dist/chart.umd.min.js"></script>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background: #0f0f1a;
      color: #e0e0f0;
      font-family: system-ui, sans-serif;
      display: flex; flex-direction: column;
      align-items: center; justify-content: center;
      min-height: 100vh; padding: 24px;
    }
    h1 { font-size: 1.2rem; color: #a0a0d0; margin-bottom: 20px; text-align: center; }
    .wrap { width: 100%; max-width: 700px; background: #1a1a2e;
            border-radius: 12px; padding: 24px; }
    canvas { max-height: 420px; }
    .hint { font-size: 0.75rem; color: #6060a0; margin-top: 14px; text-align: center; }
  </style>
</head>
<body>
<div class="wrap">
  <h1>{{TITULO}}</h1>
  <canvas id="chart"></canvas>
  <p class="hint">Hover para ver valores</p>
</div>
<script>
const ctx = document.getElementById("chart").getContext("2d");

const PALETTE = [
  "#7C3AED","#0EA5E9","#10B981","#F59E0B",
  "#EF4444","#EC4899","#6366F1","#14B8A6"
];

// {{CHART_CONFIG}}
new Chart(ctx, config);
</script>
</body>
</html>
```

### Paso 4: Configs por tipo

**Barras (`bar` / `barh`):**
```js
const config = {
  type: "bar",  // cambiar a "bar" con indexAxis:"y" para horizontal
  data: {
    labels: [/* etiquetas */],
    datasets: [{ label: "{{EJE_Y}}", data: [/* valores */],
      backgroundColor: PALETTE.map(c => c + "cc"),
      borderColor: PALETTE, borderWidth: 1 }]
  },
  options: {
    indexAxis: "x",  // "y" para horizontal
    plugins: { legend: { labels: { color: "#a0a0d0" } } },
    scales: {
      x: { ticks: { color: "#8080b0" }, grid: { color: "#2a2a4a" } },
      y: { ticks: { color: "#8080b0" }, grid: { color: "#2a2a4a" } }
    }
  }
};
```

**Líneas (`line`):**
```js
const config = {
  type: "line",
  data: {
    labels: [/* fechas o categorías */],
    datasets: [{ label: "{{SERIE}}", data: [/* valores */],
      borderColor: PALETTE[0], backgroundColor: PALETTE[0] + "33",
      fill: true, tension: 0.4, pointRadius: 4 }]
  },
  options: { plugins: { legend: { labels: { color: "#a0a0d0" } } },
    scales: { x: { ticks: { color: "#8080b0" }, grid: { color: "#2a2a4a" } },
              y: { ticks: { color: "#8080b0" }, grid: { color: "#2a2a4a" } } } }
};
```

**Pastel / Donut (`pie` / `donut`):**
```js
const config = {
  type: "doughnut",  // "pie" para pastel sólido
  data: {
    labels: [/* categorías */],
    datasets: [{ data: [/* porcentajes o valores */],
      backgroundColor: PALETTE, borderColor: "#0f0f1a", borderWidth: 3 }]
  },
  options: {
    plugins: {
      legend: { position: "bottom", labels: { color: "#a0a0d0", padding: 16 } },
      tooltip: { callbacks: {
        label: ctx => ` ${ctx.label}: ${ctx.parsed.toLocaleString()}`
      }}
    }
  }
};
```

**Dispersión (`scatter`):**
```js
const config = {
  type: "scatter",
  data: {
    datasets: [{ label: "{{SERIE}}", data: [{ x: 1, y: 2 }, ...],
      backgroundColor: PALETTE[0] + "bb", pointRadius: 7 }]
  },
  options: { plugins: { legend: { labels: { color: "#a0a0d0" } } },
    scales: { x: { title: { display: true, text: "{{EJE_X}}", color: "#8080b0" },
                   ticks: { color: "#8080b0" }, grid: { color: "#2a2a4a" } },
              y: { title: { display: true, text: "{{EJE_Y}}", color: "#8080b0" },
                   ticks: { color: "#8080b0" }, grid: { color: "#2a2a4a" } } } }
};
```

## Reglas de diseño

- Fondo siempre oscuro (`#0f0f1a`) — se ve bien en el panel de Claude
- Usar la paleta PALETTE en orden para series múltiples
- Añadir `+ "cc"` al hex para transparencia en rellenos
- Grids siempre `#2a2a4a` (sutil)
- Ticks y leyendas en `#a0a0d0` / `#8080b0`
- Hover tooltip siempre activado
- Canvas máximo 420px de alto para que quepa en el panel

## Respuesta post-gráfico

Después de publicar el Artifact:
1. Una línea con qué graficó y cuántos puntos de datos
2. Observación clave de los datos (el mayor, la tendencia, la categoría dominante)
3. Ofrecer: "¿Quieres cambiar el tipo, agregar más datos, o comparar series?"

## Si faltan datos

```
No tengo los datos para "{{DESCRIPCION}}". Puedes:
1. Pegarlos aquí (tabla, CSV, lista)
2. Decirme los números y yo los estructuro
3. Usar datos de ejemplo — escribe "ejemplo" y graficamos
```
