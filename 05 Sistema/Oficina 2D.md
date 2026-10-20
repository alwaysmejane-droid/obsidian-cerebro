# Oficina 2D (The Whales Office)

Estado al 2026-10-15. Archivo: `Agentes/static/iso2.html`. Respaldos en `Agentes/_archivo_viejo/`.

## Hecho
- Vista 2D de frente, 2D por defecto; la 3D sigue con su botón.
- Departamentos agrupados con alfombra de color y cartel flotante; mesa de reuniones ovalada al centro.
- Sillas alineadas a la mesa y a los escritorios.
- Chencho limpia todo el lugar con el trapeador.
- Charlas por turnos en burbujas de chat, con cola hacia la persona.
- Chat por persona: al pinchar a alguien, responde con datos reales (`/api/chat_agente`, módulo `chat_agente.py`).
- Reunión de Marisol: 1 minuto cada 3 horas (9:00, 12:00, 15:00 NY, lun-vie).
- Discord: solo entradas y resultados de estrategias demo; el ruedo no envía.
- Celular: menú «☰», tarjetas de una columna, botones grandes.
- Dashboard: paleta del logo con morado, cristal y neón; logo en la cabecera; fondo de barras solo detrás de la cabecera.
- Imágenes: «It's in my DNA» y toro/oso difuminados; sin velas feas.
- Acceso desde fuera: puerta de solo lectura con usuario y contraseña, publicada con Tailscale Funnel en `https://mas53.tail13b7ee.ts.net`.

## Pendiente
- Verificar en vivo en PC y celular (personas, sillas, burbujas, fondo, cabecera).
- Probar el chat por persona con datos reales.
- Confirmar que Discord recibe entradas y cierres demo.
- Probar el enlace de Funnel desde el celular.
- Historial diario de evaluación: el motor debe agregar el campo completo (`dias_det` en `fondeo_full`).

## Servidores
- Oficina: `server.py` en el puerto 8797 (reiniciado con la disposición nueva).
- Motor: `runner.py` (supervisor lo relanza).
- Puerta externa: `acceso_externo\gate.py` en 8795, apuntando a la oficina.
- Comidas: puerto 8790 (no tocado).

Relacionado: [[Pendientes]], [[Cómo parar cosas]], [[Mapa del sistema]].
