"""ORB Retest FVG — motor mecánico (traducción 1:1 de la estrategia Pine v6).

Entrada : velas de 1 minuto CERRADAS, en orden, una a una (on_bar).
Salida  : lista de eventos (Event) que un ejecutor traduce a órdenes:
          PLACE_LIMIT  -> orden límite de entrada + bracket OCO (stop y objetivo)
          CANCEL_LIMIT -> anular la límite pendiente
          FILL         -> la límite se llenó (informativo / conciliación)
          EXIT         -> salida por TP o SL (informativo / conciliación)
Sin I/O, sin reloj, sin aleatoriedad: misma secuencia de velas => mismos eventos.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Optional
from zoneinfo import ZoneInfo

NY = ZoneInfo("America/New_York")


@dataclass
class Config:
    start_hm: int = 945          # inicio del rango, HHMM Nueva York
    or_min: int = 5              # minutos del rango
    win_min: int = 120           # minutos de entradas tras el rango
    body_min: float = 0.5        # cuerpo mínimo de la vela de ruptura (0 = sin filtro)
    use_vwap: bool = False
    min_gap: float = 0.25        # FVG mínimo (× ATR)
    max_gap: float = 0.0         # 0 = sin tope
    level_mid: bool = True       # límite en la mitad del FVG (si no, en el borde)
    sl_atr: float = 1.0          # colchón del SL tras la estructura (× ATR)
    min_stop: float = 2.0        # stop mínimo (× ATR)
    rr: float = 1.0              # TP (× riesgo)
    reentry: bool = True         # una reentrada al otro lado tras SL
    max_stop_pts: float = 0.0    # 0 = sin tope
    next_fvg: bool = True        # si el TP llega antes del retest, vale el siguiente FVG
    atr_len: int = 14
    # tamaño y costes
    risk_usd: float = 400.0      # 0,8 % de 50.000 $
    tick: float = 0.25
    point_value: float = 2.0     # MNQ = 2 $/punto (NQ = 20)
    commission_per_side: float = 0.62
    slippage_ticks: int = 1

    @staticmethod
    def from_json(path: str) -> "Config":
        import json
        with open(path, encoding="utf-8") as f:
            return Config(**json.load(f))


@dataclass
class Bar:
    t: int      # epoch UTC en segundos, apertura de la vela
    o: float
    h: float
    l: float
    c: float
    v: float = 0.0


@dataclass
class Event:
    kind: str                    # PLACE_LIMIT | CANCEL_LIMIT | FILL | EXIT
    t: int                       # apertura de la vela que lo provoca
    side: int = 0                # +1 largo, -1 corto
    price: float = 0.0           # límite / fill / salida
    stop: float = 0.0
    target: float = 0.0
    qty: int = 0
    won: Optional[bool] = None
    pnl: float = 0.0             # neto de comisión y deslizamiento (sólo EXIT)
    reason: str = ""


@dataclass
class _Pending:
    side: int
    lim: float
    stop: float
    tgt: float
    qty: int


@dataclass
class _Trade:
    side: int
    entry: float
    stop: float
    tgt: float
    qty: int


def _round_half_up(x: float) -> int:
    return int(math.floor(x + 0.5))


class OrbFvgEngine:
    NO_ORDER = 0   # modos: 0 busca ruptura · 1 ruptura viva · 2 límite pendiente · 3 operación · 4 nada más hoy

    def __init__(self, cfg: Config | None = None):
        self.cfg = cfg or Config()
        c = self.cfg
        self.s_min = (c.start_hm // 100) * 60 + c.start_hm % 100
        self.mi = 0
        self.last_t = 0
        self.trs: list[float] = []
        self.prev_c: Optional[float] = None
        self.pv = 0.0
        self.vv = 0.0
        self.fut_day = 0
        self.b1: Optional[tuple[float, float, int]] = None  # (h, l, índice) vela anterior
        self.b2: Optional[tuple[float, float, int]] = None  # vela de hace dos
        # sesión
        self.s_date = 0
        self.s_valid = False
        self.s_hi = self.s_lo = 0.0
        self.s_or_end = False
        self.mode = 0
        self.side = 0          # restricción de dirección tras reentrada
        self.round = 0
        self.brk_mi = -1
        self.up = False
        self.pend: Optional[_Pending] = None
        self.open: Optional[_Trade] = None

    # ── utilidades ────────────────────────────────────────────────
    def _qty(self, risk_pts: float) -> int:
        return max(1, _round_half_up(self.cfg.risk_usd / (risk_pts * self.cfg.point_value)))

    def _cost(self, q: int) -> float:
        c = self.cfg
        return q * (2 * c.commission_per_side + 2 * c.slippage_ticks * c.tick * c.point_value)

    def _pnl(self, tr: _Trade, px: float) -> float:
        return tr.side * (px - tr.entry) * tr.qty * self.cfg.point_value - self._cost(tr.qty)

    # ── una vela cerrada ─────────────────────────────────────────
    def on_bar(self, bar: Bar) -> list[Event]:
        ev: list[Event] = []
        c = self.cfg
        if bar.t <= self.last_t:
            return ev                       # vela repetida o desordenada: se ignora
        self.last_t = bar.t
        self.mi += 1
        t, o, h, l, cl = bar.t, bar.o, bar.h, bar.l, bar.c
        v = max(bar.v or 0.0, 0.0)

        # ATR simple (rango verdadero) y VWAP del día de futuros (cambia a las 18:00 NY)
        tr = (h - l) if self.prev_c is None else max(h, self.prev_c) - min(l, self.prev_c)
        self.trs.append(tr)
        if len(self.trs) > c.atr_len:
            self.trs.pop(0)
        atr = sum(self.trs) / len(self.trs)
        dt_ny = datetime.fromtimestamp(t, timezone.utc).astimezone(NY)
        fd = (dt_ny + timedelta(hours=6)).date().toordinal()
        if fd != self.fut_day:
            self.fut_day, self.pv, self.vv = fd, 0.0, 0.0
        self.pv += (h + l + cl) / 3 * v
        self.vv += v
        vwap = self.pv / self.vv if self.vv > 0 else cl

        rel = dt_ny.hour * 60 + dt_ny.minute - self.s_min
        dt = dt_ny.year * 10000 + dt_ny.month * 100 + dt_ny.day
        in_win = (self.s_valid and self.s_or_end and dt == self.s_date
                  and c.or_min <= rel < c.or_min + c.win_min)
        last_w = rel == c.or_min + c.win_min - 1
        skip = False

        # 1) operación abierta: SL primero; con hueco, a la apertura
        if self.mode == 3 and self.open:
            tr_ = self.open
            d = tr_.side
            xp = None
            reason = ""
            if (l <= tr_.stop) if d > 0 else (h >= tr_.stop):
                xp = min(o, tr_.stop) if d > 0 else max(o, tr_.stop)
                reason = "SL"
            elif (h >= tr_.tgt) if d > 0 else (l <= tr_.tgt):
                xp = max(o, tr_.tgt) if d > 0 else min(o, tr_.tgt)
                reason = "TP"
            if xp is not None:
                won = d * (xp - tr_.entry) > 0
                ev.append(Event("EXIT", t, d, xp, tr_.stop, tr_.tgt, tr_.qty, won, self._pnl(tr_, xp), reason))
                if not won and c.reentry and self.round == 0 and in_win and not last_w:
                    self.mode, self.round, self.side = 0, 1, -d
                else:
                    self.mode = 4
                self.open = None
                skip = True

        # 2) sesión del día (rango de apertura)
        if 0 <= rel < c.or_min + c.win_min and dt != self.s_date:
            self.s_date = dt
            self.s_valid = rel < c.or_min
            self.s_hi, self.s_lo = h, l
            self.s_or_end = False
            if self.mode != 3:
                self.mode = 0
            self.side = 0
            self.round = 0

        if self.s_valid and dt == self.s_date and 0 <= rel < c.or_min:
            self.s_hi = max(self.s_hi, h)
            self.s_lo = min(self.s_lo, l)
            if rel + 1 >= c.or_min:
                self.s_or_end = True
        elif in_win and not skip and self.mode == 2:
            self._pending_bar(bar, last_w, ev)
        elif in_win and not skip and self.mode == 1:
            self._live_breakout_bar(bar, atr, last_w, ev)
        elif in_win and not skip and self.mode == 0:
            self._find_breakout(bar, vwap)

        if in_win and last_w and self.mode in (0, 1):
            self.mode = 4

        # 3) desplazar las dos velas anteriores
        self.b2 = self.b1
        self.b1 = (h, l, self.mi)
        self.prev_c = cl
        return ev

    # ── modo 2: límite pendiente ────────────────────────────────
    def _pending_bar(self, bar: Bar, last_w: bool, ev: list[Event]) -> None:
        p = self.pend
        assert p is not None
        d, o, h, l, t = p.side, bar.o, bar.h, bar.l, bar.t
        if (l <= p.lim) if d > 0 else (h >= p.lim):
            ep = min(o, p.lim) if d > 0 else max(o, p.lim)
            self.open = _Trade(d, ep, p.stop, p.tgt, p.qty)
            self.pend = None
            self.mode = 3
            ev.append(Event("FILL", t, d, ep, p.stop, p.tgt, p.qty))
            # en la vela del llenado sólo cuenta el SL
            if (l <= p.stop) if d > 0 else (h >= p.stop):
                xp = min(o, p.stop) if d > 0 else max(o, p.stop)
                ev.append(Event("EXIT", t, d, xp, p.stop, p.tgt, p.qty, False, self._pnl(self.open, xp), "SL"))
                self.open = None
                if self.cfg.reentry and self.round == 0 and not last_w:
                    self.mode, self.round, self.side = 0, 1, -d
                else:
                    self.mode = 4
        elif (h >= p.tgt) if d > 0 else (l <= p.tgt):
            ev.append(Event("CANCEL_LIMIT", t, d, p.lim, reason="TP antes del retest"))
            self.pend = None
            self.mode = 1 if self.cfg.next_fvg else 4
        elif last_w:
            ev.append(Event("CANCEL_LIMIT", t, d, p.lim, reason="fin de ventana"))
            self.pend = None
            self.mode = 4

    # ── modo 1: ruptura viva, buscar el primer FVG a favor ──────
    def _live_breakout_bar(self, bar: Bar, atr: float, last_w: bool, ev: list[Event]) -> None:
        c = self.cfg
        h, l, cl, t = bar.h, bar.l, bar.c, bar.t
        if self.s_lo <= cl <= self.s_hi:
            self.mode = 0                         # volvió a cerrar dentro: ruptura olvidada
            return
        up = self.up
        if self.b2 is None or self.mi - 1 < self.brk_mi:
            return
        h2, l2, m2 = self.b2
        gap = (l - h2) if up else (l2 - h)
        if not (gap > 0 and gap >= c.min_gap * atr and not (c.max_gap > 0 and gap > c.max_gap * atr)):
            return
        edge = l if up else h
        far = h2 if up else l2
        lim = (edge + far) / 2 if c.level_mid else edge
        lim = round(lim / c.tick) * c.tick
        # estructura: mínimo / máximo de las velas del FVG desde la ruptura
        ext = l if up else h
        if self.b1 and self.b1[2] >= self.brk_mi:
            ext = min(ext, self.b1[1]) if up else max(ext, self.b1[0])
        if m2 >= self.brk_mi:
            ext = min(ext, l2) if up else max(ext, h2)
        stop = ext - c.sl_atr * atr if up else ext + c.sl_atr * atr
        mr = c.min_stop * atr
        if (lim - stop < mr) if up else (stop - lim < mr):
            stop = lim - mr if up else lim + mr
        risk = (lim - stop) if up else (stop - lim)
        if not (risk > 0 and not (c.max_stop_pts > 0 and risk > c.max_stop_pts)):
            return
        if last_w:
            self.mode = 4                         # se forma en la última vela de la ventana: nada
            return
        tgt = lim + c.rr * risk if up else lim - c.rr * risk
        d = 1 if up else -1
        qty = self._qty(risk)
        self.pend = _Pending(d, lim, stop, tgt, qty)
        self.mode = 2
        ev.append(Event("PLACE_LIMIT", t, d, lim, stop, tgt, qty))

    # ── modo 0: primera vela que CIERRA fuera del rango ─────────
    def _find_breakout(self, bar: Bar, vwap: float) -> None:
        c = self.cfg
        o, h, l, cl = bar.o, bar.h, bar.l, bar.c
        u = cl > self.s_hi and self.side != -1
        dn = cl < self.s_lo and self.side != 1
        if not (u or dn):
            return
        rg, body = h - l, abs(cl - o)
        ok = not (c.body_min > 0 and (not rg > 0 or body / rg < c.body_min or (cl <= o if u else cl >= o)))
        if ok and c.use_vwap:
            ok = cl > vwap if u else cl < vwap
        if ok:
            self.mode, self.up, self.brk_mi = 1, u, self.mi
