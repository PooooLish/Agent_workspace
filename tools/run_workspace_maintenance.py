#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

from workspace import run_checks


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    code = run_checks(root, full=True)
    if code == 0:
        print("\nMaintenance checks completed.", flush=True)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
