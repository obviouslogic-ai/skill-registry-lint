"""Skill registry lint: every skill a file references must resolve to a real skill.

Layout:
  skills/<name>/SKILL.md   a skill
  registry.json            {"aliases": {"old-name": "new-name"}}
A reference is written as [[skill:name]] in any Markdown file under the root.
"""
import json
import re
import sys
from pathlib import Path

REF = re.compile(r"\[\[skill:([a-z0-9-]+)\]\]")


def load(root: Path):
    skills = {p.parent.name for p in (root / "skills").glob("*/SKILL.md")}
    reg = root / "registry.json"
    aliases = json.loads(reg.read_text()).get("aliases", {}) if reg.exists() else {}
    return skills, aliases


def resolve(name, skills, aliases):
    seen = set()
    while name not in skills:
        if name in seen or name not in aliases:
            return None
        seen.add(name)
        name = aliases[name]
    return name


def lint(root):
    root = Path(root)
    skills, aliases = load(root)
    problems = []
    for alias, target in aliases.items():
        if alias in skills:
            problems.append(f"registry.json: alias '{alias}' shadows a real skill")
        elif resolve(alias, skills, aliases) is None:
            problems.append(f"registry.json: alias '{alias}' -> '{target}' does not resolve")
    for md in sorted(root.rglob("*.md")):
        for n, line in enumerate(md.read_text().splitlines(), 1):
            for name in REF.findall(line):
                if resolve(name, skills, aliases) is None:
                    problems.append(f"{md.relative_to(root)}:{n}: unknown skill '{name}'")
    return problems


if __name__ == "__main__":
    problems = lint(sys.argv[1] if len(sys.argv) > 1 else ".")
    for p in problems:
        print(p)
    print("ok" if not problems else f"{len(problems)} problem(s)")
    sys.exit(1 if problems else 0)
