"""Pruebas con velas sintéticas (día de invierno, 2026-01-12, NY = UTC-5)."""
from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo

from engine import Bar, Config, OrbFvgEngine

NY = ZoneInfo("America/New_York")


def ts(h, m):
    return int(datetime(2026, 1, 12, h, m, tzinfo=NY).timestamp())


def run(bars):
    eng, out = OrbFvgEngine(Config()), []
    for b in bars:
        out += eng.on_bar(b)
    return out


def base():
    # warm-up para el ATR (08:00..09:44, rango 4 puntos) y rango 09:45-09:49 entre 100 y 104
    bars = [Bar(ts(9, 45) - 60 * k, 101, 103, 99, 101) for k in range(120, 0, -1)]
    bars += [Bar(ts(9, 45 + i), 101, 104, 100, 102) for i in range(5)]
    return bars


def fvg_bars():
    bars = base()
    bars += [Bar(ts(9, 50), 103, 108, 103, 107.5)]      # ruptura alcista, cuerpo 90 %
    bars += [Bar(ts(9, 51), 107.5, 110, 107.5, 109.5)]  # low 107.5 > high(09:49)=104 -> FVG, límite en 105.75
    return bars


def test_long_limit_and_tp():
    bars = fvg_bars()
    bars += [Bar(ts(9, 52), 109, 109, 105.5, 106)]      # toca la límite -> llenado
    bars += [Bar(ts(9, 53), 106, 140, 105.8, 139)]      # TP
    ev = run(bars)
    assert [e.kind for e in ev] == ["PLACE_LIMIT", "FILL", "EXIT"], ev
    assert ev[0].side == 1 and ev[0].price == 105.75
    assert ev[2].won and ev[2].reason == "TP"
    assert abs((ev[0].target - ev[0].price) - (ev[0].price - ev[0].stop)) < 1e-9   # 1:1


def test_breakout_forgotten_when_closing_inside():
    bars = base()
    bars += [Bar(ts(9, 50), 103, 108, 103, 107.5)]
    bars += [Bar(ts(9, 51), 107.5, 108, 100, 102)]    # vuelve dentro -> ruptura olvidada
    bars += [Bar(ts(9, 52), 102, 103, 101, 102)]
    assert run(bars) == []


def test_weak_body_is_not_breakout():
    bars = base()
    bars += [Bar(ts(9, 50), 104, 110, 100, 105)]      # cuerpo 10 % < 50 %
    assert run(bars) == []


def test_sl_loses_and_stops_when_no_reentry_pattern():
    bars = fvg_bars()
    bars += [Bar(ts(9, 52), 109, 109, 105.5, 106)]      # llenado
    bars += [Bar(ts(9, 53), 106, 106, 60, 62)]          # SL
    ev = run(bars)
    assert [e.kind for e in ev] == ["PLACE_LIMIT", "FILL", "EXIT"], ev
    assert not ev[2].won and ev[2].reason == "SL" and ev[2].pnl < 0


def test_tp_before_retest_cancels_limit():
    bars = fvg_bars()
    bars += [Bar(ts(9, 52), 109, 130, 109, 129)]        # sube al TP sin tocar la límite
    ev = run(bars)
    assert [e.kind for e in ev] == ["PLACE_LIMIT", "CANCEL_LIMIT"], ev


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
