"""Loop + Goal Agent Skills — `loop-skills` installer and `loop-init` scaffolder."""
from __future__ import annotations

import argparse
import datetime
import shutil
import sys
from pathlib import Path

_PKG = Path(__file__).resolve().parent
_SKILLS = _PKG / "_skills"  # bundled at build time: _skills/loop, _skills/goal
SKILL_NAMES = ("loop", "goal")
WIKI_FILES = [
    "index.md", "overview.md", "decisions.md",
    "architecture.md", "learnings.md", "glossary.md",
]


def _skills_root() -> Path:
    if not _SKILLS.exists():
        sys.exit(f"ERROR: bundled skills not found at {_SKILLS}. Try reinstalling the package.")
    return _SKILLS


def install(args) -> int:
    root = _skills_root()
    if args.dest:
        dest = Path(args.dest).expanduser().resolve()
    elif args.project:
        dest = Path.cwd() / ".claude" / "skills"
    else:
        dest = Path.home() / ".claude" / "skills"
    dest.mkdir(parents=True, exist_ok=True)
    print(f"Installing skills into: {dest}")
    for name in SKILL_NAMES:
        src = root / name
        if not src.exists():
            print(f"  warn: missing bundled skill: {name}")
            continue
        shutil.copytree(src, dest / name, dirs_exist_ok=True)
        print(f"  installed: {dest / name}")
    print("\nDone. Start a new Claude Code session; invoke with /loop and /goal.")
    return 0


def _fill(text: str, ctx: dict) -> str:
    for key, val in ctx.items():
        text = text.replace("{{" + key + "}}", val)
    return text


def _write(dest: Path, content: str, force: bool) -> None:
    if dest.exists() and not force:
        print(f"  skip (exists): {dest}")
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(content, encoding="utf-8")
    print(f"  wrote: {dest}")


def init(args) -> int:
    assets = _skills_root() / "loop" / "assets"
    if not assets.exists():
        sys.exit(f"ERROR: templates not found at {assets}")
    proj = Path(args.project_dir).expanduser().resolve()
    proj.mkdir(parents=True, exist_ok=True)
    ctx = {
        "PROJECT_NAME": args.name or proj.name,
        "ONE_LINE_MISSION": args.mission or "<one line>",
        "OWNER": args.owner or "<owner>",
        "DATE": datetime.date.today().isoformat(),
    }
    print(f"Initializing Loop state in: {proj}")
    _write(proj / "LOOP_STATE.md",
           _fill((assets / "LOOP_STATE.template.md").read_text(encoding="utf-8"), ctx),
           args.force)
    for fname in WIKI_FILES:
        src = assets / "wiki" / fname
        if src.exists():
            _write(proj / "wiki" / fname,
                   _fill(src.read_text(encoding="utf-8"), ctx), args.force)
    print("\nDone. Open LOOP_STATE.md and define your first iteration goal (PLAN).")
    return 0


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="loop-skills",
                                description="Install the Loop + Goal Agent Skills into your Claude skills directory.")
    sub = p.add_subparsers(dest="cmd", required=True)
    pi = sub.add_parser("install", help="Copy the loop + goal skills into your Claude skills dir.")
    pi.add_argument("--project", action="store_true",
                    help="Install into ./.claude/skills (this repo/project) instead of ~/.claude/skills")
    pi.add_argument("--dest", help="Custom destination directory")
    pi.set_defaults(func=install)
    args = p.parse_args(argv)
    return args.func(args)


def init_main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="loop-init",
                                description="Scaffold Loop state (LOOP_STATE.md + wiki/) into a project folder.")
    p.add_argument("project_dir", help="Target project folder")
    p.add_argument("--name", help="Project name (default: folder name)")
    p.add_argument("--mission", help="One-line mission")
    p.add_argument("--owner", default="", help="Project owner")
    p.add_argument("--force", action="store_true", help="Overwrite existing files")
    args = p.parse_args(argv)
    return init(args)


if __name__ == "__main__":
    raise SystemExit(main())
