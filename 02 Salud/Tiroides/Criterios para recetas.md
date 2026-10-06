# Criterios para recetas (base para rehacer la web de Comidas)

Volver a [[00 Tiroides]] · [[Dieta]] · App: [[Comidas]]

Objetivo: la web solo debe tener recetas de **desayuno, almuerzo y cena** que encajen con la tiroides. Estas reglas sirven para clasificar cada receta y filtrar las que no.

## Perfil único
**Hipotiroidismo.** Toda la web responde a lo saludable para alguien con hipotiroidismo. No hay modos ni perfiles separados: una receta entra solo si encaja, y si no, no está. (Decisión 2026-10-04.)

Además: una **lista de ingredientes prohibidos** que bloquea cualquier receta que los lleve, sin excepciones.

## Reglas para ACEPTAR una receta
1. Base de verduras o legumbres, y una proteína (pescado, pollo, huevo, legumbres, pavo, carne magra).
2. Grasas buenas: aceite de oliva, aguacate, frutos secos.
3. Carbohidrato complejo: arroz integral, quinoa, avena, papa/boniato, legumbres.
4. Cocción simple (horno, plancha, vapor, guiso); fritura ocasional.
5. Pocos ultraprocesados y poca azúcar añadida.

## Etiquetas por receta (campos a añadir en la base de datos)
| Campo | Valores | Para qué |
|---|---|---|
| `comida` | desayuno / almuerzo / cena | Ya pedido |
| `yodo` | bajo / medio / alto | Evitar exceso (Hashimoto) |
| `selenio` | si / no | Resaltar nueces de Brasil, atún, huevo… |
| `fibra_alta` | si / no | Aviso: lejos de la pastilla (4 h) |
| `soja` | si / no | Aviso: lejos de la pastilla |
| `calcio_alto` | si / no | Aviso: lejos de la pastilla |
| `cruciferas` | si / no | Recordar que cocidas están bien |
| `gluten` | si / no | Filtro opcional (celiaquía) |
| `tiempo_min` | número | Practicidad |
| `proteina_principal` | pollo / pescado / huevo / legumbres / carne / veg | Ya existe como categoría |

## Reglas para EXCLUIR o marcar
- **Hipotiroidismo / Hashimoto:** excluir algas y suplementos de kelp (exceso de yodo); marcar soja y fibra alta con aviso de horario.
- **Prohibidos:** cualquier receta con un ingrediente de la lista prohibida se bloquea.
- **Todos:** sacar postres azucarados, ultraprocesados y frituras pesadas del flujo principal.

## Estructura de día sugerida (para el menú)
- **Desayuno** (60 min después de la pastilla): huevo + verdura, avena con fruta y frutos secos, yogur con nueces y bayas, tortilla de claras (hiper).
- **Almuerzo:** plato de verduras + proteína + carbohidrato complejo; legumbres 3–4 veces por semana.
- **Cena:** ligera, pescado o pollo con verduras; cena 3 h antes de dormir si toma levotiroxina de noche.
- **Merienda (opcional):** fruta + 1–2 nueces de Brasil; evitar café con calcio justo después de la pastilla.

## Variedad semanal (reglas del sorteo)
- Pescado 2 veces.
- Pollo/pavo 2–3 veces, legumbres 3 veces, huevo 2 veces, carne roja 1 vez.
- No repetir proteína dos días seguidos.

## Cambios a la web (para después)
1. Recortar la base de recetas a las que cumplan las reglas y etiquetarlas.
2. Pestañas: Desayuno / Almuerzo / Cena (en vez de cena única).
3. Pestaña de **ingredientes prohibidos** que bloquea recetas.
4. Avisos automáticos de horario con la medicación.
5. Lista de compra por pasillos (ya existe).
6. Sorteo semanal por reglas de variedad.

Ver también: [[Medicamentos]] (horarios), [[Estilo de vida]].

## Fuentes
- [Mediterranean diet and Hashimoto's](https://www.palomahealth.com/learn/mediterranean-diet-hashimotos)
- [7-day Hashimoto's plan (RD)](https://www.nourish.com/blog/hashimotos-meal-plan)
- [Hyperthyroidism diet (Healthgrades)](https://resources.healthgrades.com/right-care/thyroid-disorders/hyperthyroidism-diet)
- [Levothyroxine y fibra](https://www.doctronic.ai/blog/levothyroxine-and-high-fiber-diet/)

Volver a [[Salud]]
