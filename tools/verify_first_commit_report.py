#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
from pathlib import Path


GENERATED_PREFIX = "Generated: "


def load_report_generator(root: Path):
    path = root / "tools" / "prepare_first_commit_report.py"
    spec = importlib.util.spec_from_file_location("prepare_first_commit_report", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Cannot load tools/prepare_first_commit_report.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def normalize_generated_line(text: str) -> str:
    lines = []
    for line in text.splitlines():
        if line.startswith(GENERATED_PREFIX):
            lines.append(f"{GENERATED_PREFIX}<ignored>")
        else:
            lines.append(line)
    return "\n".join(lines)


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    report_path = root / "outputs" / "first_commit_recommendation.md"
    if not report_path.exists():
        print("outputs/first_commit_recommendation.md is missing.")
        return 1

    generator = load_report_generator(root)
    expected = generator.build_report(root, generator.candidate_files(root))
    actual = report_path.read_text(encoding="utf-8")

    if normalize_generated_line(actual) != normalize_generated_line(expected):
        print("outputs/first_commit_recommendation.md is stale. Run:")
        print("  python tools/prepare_first_commit_report.py")
        return 1

    print("outputs/first_commit_recommendation.md is current.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
