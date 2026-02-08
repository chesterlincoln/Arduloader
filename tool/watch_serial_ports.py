#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Poll serial ports and print changes (added/removed).
"""

import time
from serial.tools import list_ports


def _snapshot():
    return {p.device for p in list_ports.comports()}


def main(interval=1.0):
    known = _snapshot()
    print("Watching serial ports. Interval: %.1fs" % interval)
    if not known:
        print("No ports detected. Waiting for changes...")
    else:
        print("Initial ports:", ", ".join(sorted(known)))
    while True:
        time.sleep(interval)
        current = _snapshot()
        added = sorted(current - known)
        removed = sorted(known - current)
        for dev in added:
            print("ADDED:", dev)
        for dev in removed:
            print("REMOVED:", dev)
        known = current


if __name__ == "__main__":
    raise SystemExit(main())
