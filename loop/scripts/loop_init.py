#!/usr/bin/env python3
"""
loop_init.py — scaffold Loop's persistent state into a project folder.

Creates LOOP_STATE.md and a wiki/ directory from the bundled asset templates,
filling in project name, mission, owner, and today's date. Idempotent: refuses
to overwrite existing files unless --force is passed.

Usage:
    python loop_init.py <project-dir> [--name NAME] [--mission TEXT]
                        [--owner NAME] [--force]

Examples:
    python loop_init.py ./ParryAI --name ParryAI \
        --mission "Prompt-injection armor for LLM apps" --owner Jesse
    python loop_init.py .          # interactive prompts for missing fields
"""
import argparse
import datetime
import sys
from pathlib import Path

# Templates live alongside this script: ../assets/
ASSETS = Path(__file__).resolve().parent.parent / "assets"

WIKI_FILES = [
    "index.md",
    "overview.md",
    "decisions.md",
    "architecture.md",
    "learnings.md",
    "glossary.md",
]


def fill(text: str, ctx: dict) -> str:
    for key, val in ctx.items():
        text = text.replace("{{" + key + "}}", val)
    return text


def write(dest: Path, content: str, force: bool) -> bool:
    if dest.exists() and not force:
        print(f"  skip (exists): {dest}")
        return False
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(content, encoding="utf-8")
    print(f"  wrote: {dest}")
    return True


def main() -> int:
    ap = argparse.ArgumentParser(description="Scaffold Loop state into a project.")
    ap.add_argument("project_dir", help="Target project folder")
    ap.add_argument("--name", help="Project name")
    ap.add_argument("--mission", help="One-line mission")
    ap.add_argument("--owner", default="", help="Project owner")
    ap.add_argument("--force", action="store_true", help="Overwrite existing files")
    args = ap.parse_args()

    proj = Path(args.project_dir).resolve()
    proj.mkdir(parents=True, exist_ok=True)

    name = args.name or input(f"Project name [{proj.name}]: ").strip() or proj.name
    mission = args.mission or input("One-line mission: ").strip() or "<one line>"
    owner = args.owner or input("Owner (optional): ").strip()

    if not ASSETS.exists():
        print(f"ERROR: asset templates not found at {ASSETS}", file=sys.stderr)
        return 1

    ctx = {
        "PROJECT_NAME": name,
        "ONE_LINE_MISSION": mission,
        "OWNER": owner or "<owner>",
        "DATE": datetime.date.today().isoformat(),
    }

    print(f"Initializing Loop state in: {proj}")

    # LOOP_STATE.md
    tmpl = (ASSETS / "LOOP_STATE.template.md").read_text(encoding="utf-8")
    write(proj / "LOOP_STATE.md", fill(tmpl, ctx), args.force)

    # wiki/
    for fname in WIKI_FILES:
        src = ASSETS / "wiki" / fname
        if not src.exists():
            print(f"  warn: template missing: {src}")
            continue
        write(proj / "wiki" / fname, fill(src.read_text(encoding="utf-8"), ctx), args.force)

    print("\nDone. Open LOOP_STATE.md and define your first iteration goal (PLAN).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
