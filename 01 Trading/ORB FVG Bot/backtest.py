"""Backtest / réplica: lee velas de 1 min en CSV y emite los eventos del motor.

CSV con cabecera: time,open,high,low,close,volume   (time = epoch UTC en segundos, o ISO-8601)
Uso: python backtest.py velas.csv [config.json]
"""
import csv
import sys
from datetime import datetime

from engine import Bar, Config, OrbFvgEngine


def _ts(s: str) -> int:
    try:
        return int(float(s))
    except ValueError:
        return int(datetime.fromisoformat(s.replace("Z", "+00:00")).timestamp())


def run(path: str, cfg: Config):
    eng = OrbFvgEngine(cfg)
    exits = []
    with open(path, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            bar = Bar(_ts(r["time"]), float(r["open"]), float(r["high"]), float(r["low"]),
                      float(r["close"]), float(r.get("volume") or 0))
            for e in eng.on_bar(bar):
                print(f'{datetime.utcfromtimestamp(e.t):%Y-%m-%d %H:%M}Z {e.kind:12} side={e.side:+d} '
                      f'px={e.price:.2f} sl={e.stop:.2f} tp={e.target:.2f} qty={e.qty} {e.reason}')
                if e.kind == "EXIT":
                    exits.append(e)
    n = len(exits)
    w = sum(1 for e in exits if e.won)
    print(f"\n{n} operaciones · {w} TP / {n - w} SL · neto {sum(e.pnl for e in exits):,.0f} $")


if __name__ == "__main__":
    run(sys.argv[1], Config.from_json(sys.argv[2]) if len(sys.argv) > 2 else Config())
