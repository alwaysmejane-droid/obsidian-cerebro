# ORB Retest FVG — versión mecánica (MNQ / NQ, 1 min)

Traducción de la estrategia Pine «ORB Retest FVG · 09:45 5m · 1 min · TP 1:1» a un motor sin dibujo, sin histórico incrustado y sin ambigüedad. Código en `engine.py`; parámetros en `config.json`.

## Contrato
- **Entrada**: velas de 1 min *cerradas*, en orden, con `time` (epoch UTC, apertura), `open/high/low/close/volume`.
- **Salida**: eventos `PLACE_LIMIT`, `CANCEL_LIMIT`, `FILL`, `EXIT`. El ejecutor sólo traduce eventos a órdenes del bróker.
- Determinista: misma secuencia de velas → mismos eventos. Velas repetidas o desordenadas se ignoran.

## Reglas (hora de Nueva York)
1. **Rango**: máximo y mínimo de las velas de 09:45 a 09:49. Si la 1.ª vela vista del día ya está pasada del rango, ese día no opera.
2. **Ventana de entradas**: 120 min desde las 09:50 (09:50–11:49).
3. **Ruptura**: 1.ª vela que *cierra* fuera del rango con cuerpo ≥ 50 % de (high−low) y de su color (alcista arriba, bajista abajo). Si luego cierra dentro del rango antes del FVG, la ruptura se olvida y se busca otra.
4. **FVG a favor**: velas A, B, C consecutivas con B posterior o igual a la ruptura. Largo: `low(C) − high(A) > 0`; corto: `low(A) − high(C) > 0`. Hueco ≥ 0,25 × ATR(14) (media simple del rango verdadero, incluida C).
5. **Orden límite** (al cerrar C) en la mitad del hueco, redondeada al tick. Vive hasta el fin de la ventana.
6. **Stop**: extremo (mínimo en largo / máximo en corto) de A, B, C contando sólo velas desde la ruptura, ∓ 1 ATR. Distancia mínima límite→stop = 2 ATR. **TP** = límite ± 1 × riesgo.
7. **Tamaño**: `contratos = max(1, round(400 $ / (riesgo en puntos × 2 $)))`, redondeo .5 hacia arriba (MNQ; NQ: `point_value = 20`).
8. **Llenado**: a partir de la vela *siguiente* a C, si el precio toca la límite. Precio = mejor de apertura y límite. En esa vela sólo cuenta el SL.
9. **Límite sin llenar**: si toca el TP antes del retest → se anula y vale el siguiente FVG (la ruptura sigue viva). Si acaba la ventana → se anula.
10. **Salidas**: sólo SL o TP, sin break-even, parciales ni cierre horario. Si una vela toca ambos, SL primero. Con hueco, sale a la apertura.
11. **Tras la salida**: TP → nada más ese día. SL dentro de la ventana (no en su última vela) → UNA reentrada, sólo al lado contrario, con el mismo patrón desde la vela siguiente. Segundo SL → fin del día.
12. Una FVG formada en la última vela de la ventana no genera orden.

## Interfaz de ejecución (lo que hace el sistema)
| Evento | Acción en el bróker |
|---|---|
| `PLACE_LIMIT` (side, price, qty, stop, target) | Enviar bracket: límite de entrada + OCO stop/objetivo, validez hasta fin de ventana |
| `CANCEL_LIMIT` | Cancelar la límite si sigue viva |
| `FILL` / `EXIT` | Conciliar con el bróker; si difieren, manda el bróker y se registra la discrepancia |

Salvaguardas recomendadas para el ejecutor (no están en la estrategia): máx. 1 posición, bloqueo diario tras 2 SL, rechazo de datos con huecos de más de 1 min, y cierre manual si queda posición tras el fin de sesión.

## Qué no se ha traducido
- Dibujo, panel, tabla mensual, alertas y las 239 operaciones históricas incrustadas (en Pine sólo servían para pintar y contar).
- El probador de TradingView usa la cantidad del precio de llenado; aquí se fija al emitir la límite (idéntica salvo huecos).

## Uso
```
python test_engine.py                      # pruebas sintéticas
python backtest.py velas.csv config.json   # réplica sobre CSV (time,open,high,low,close,volume)
```
## Pendiente
Validar contra el CSV de Acrox (239 operaciones, 01-01 → 10-11-2026): no está en este repositorio, así que la equivalencia con el Pine es por lectura del código, no comprobada con datos.
