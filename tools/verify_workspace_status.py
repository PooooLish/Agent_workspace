#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
from pathlib import Path


def load_status_generator(root: Path):
    path = root / "tools" / "generate_workspace_status.py"
    spec = importlib.util.spec_from_file_location("generate_workspace_status", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Cannot load tools/generate_workspace_status.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    status_path = root / "WORKSPACE_STATUS.md"
    if not status_path.exists():
        print("WORKSPACE_STATUS.md is missing.")
        return 1

    generator = load_status_generator(root)
    expected = generator.build_status(root)
    actual = status_path.read_text(encoding="utf-8")

    if actual != expected:
        print("WORKSPACE_STATUS.md is stale. Run:")
        print("  python tools/generate_workspace_status.py")
        return 1

    print("WORKSPACE_STATUS.md is current.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
