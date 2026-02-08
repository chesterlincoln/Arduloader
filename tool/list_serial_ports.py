#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
List serial ports and print detailed metadata from pyserial.
"""

from serial.tools import list_ports


def main():
    ports = list_ports.comports()
    if not ports:
        print("NO_PORTS")
        return 0
    for p in ports:
        print("PORT:", p.device)
        print("  desc:", p.description)
        print("  hwid:", p.hwid)
        print("  vid:", getattr(p, "vid", None))
        print("  pid:", getattr(p, "pid", None))
        print("  manufacturer:", getattr(p, "manufacturer", None))
        print("  product:", getattr(p, "product", None))
        print("  serial_number:", getattr(p, "serial_number", None))
        print("  location:", getattr(p, "location", None))
        print("---")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
