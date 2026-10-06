# Cómo parar cosas

- **Bitunix real:** crear un archivo llamado `LIVE_STOP` en `Bitunix Proyecto`. No entran operaciones nuevas (las abiertas siguen con su SL/TP). Para apagar del todo: quitar `BITUNIX_LIVE_TRADING` del `.env` y reiniciar `bitunix-lab`.
- **Cualquier servicio:** acción `parar` al supervisor (ver [[Mapa del sistema]]).
- **Cerrar una posición ya abierta:** a mano en la app de Bitunix.
