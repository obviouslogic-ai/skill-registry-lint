# skill-registry-lint

A small linter for a library of agent skills. Docs and skills point at other skills with `[[skill:name]]`. When a skill is renamed or removed, those pointers quietly break, and an agent ends up following instructions that lead nowhere. This tool finds them before that happens.

## What it checks

- Every `[[skill:name]]` in any Markdown file resolves to `skills/<name>/SKILL.md`, directly or through an alias.
- Every alias in `registry.json` ends at a real skill (no dead ends, no cycles).
- No alias has the same name as a real skill.

It exits with code 1 when anything is wrong, so it can run in CI or a pre-commit hook.

## Run it

```
python3 lint.py example
```

The example has one dead alias and one reference to a skill that does not exist.

## Test it

```
python3 -m unittest -v
```

Python 3.10+, standard library only.

## Demo

Terminal recording: `demo.cast` (play with `asciinema play demo.cast`).
