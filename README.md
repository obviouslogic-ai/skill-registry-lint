# skill-registry-lint

A linter that checks every `[[skill:name]]` reference and alias in a skill library resolves to a real skill.

**This is a scripted demo that represents the process** I run in my own agent framework. It is not a sample or excerpt of that system, and none of its code or data is in it.

- Live page: https://demos.obviouslogic.ai/skill-registry-lint/
- Source: https://github.com/obviouslogic-ai/skill-registry-lint

## Why I built this

Agents follow playbooks that call skills by name. When a skill is renamed or never written, the agent does not crash. It skips the step, finishes and reports success, run after run, until someone downstream notices. My own agents work from a shared skill library where renamed skills keep aliases, and every playbook is linted before it ships. This repo acts that out on a tiny `example/` library.

## The cost, before and after the lint

The page has an illustrative cost model. Every number is an input you can change; none are measured or cited figures.

- No lint: runs a week x weeks before anyone notices = silent failures, x minutes to redo one run x hourly rate.
- Lint first: one fix, minutes to fix x hourly rate.
- Defaults: 25 runs a week, 6 weeks, 30 minutes a redo, $75 an hour, 15 minutes to fix. That is 150 silent failures and $5,625 without the lint, $19 with it.

## Run the CLI

```sh
python3 lint.py example   # lists broken references, exits 1 if any
```

Standard library only, no installs.

## Run the page locally

```sh
cd web && ./get-pyodide.sh && cd ..   # once: downloads Pyodide 0.27.7 into web/vendor (gitignored)
python3 -m http.server 8000   # from the folder that holds this repo
# open http://localhost:8000/skill-registry-lint/web/
```

The page fits one screen. Press **Run it both ways**. Before: the agent walks `docs/onboarding.md` with the same `resolve()` the lint uses, the `publish` step is skipped without an error, the run reports success, and a tape of runs fills in, all green and all incomplete. After: the lint runs before the playbook ships, the reference graph draws in with broken references in red, two scripted fixes are applied, the lint runs clean and the runs complete. The explanation sits behind **About this demo** in the corner. Add `?fast=1` to skip the pauses.

The page runs this repo's real Python in the browser through Pyodide, so what you click is the same code the tests cover. Styling comes from `web/kit/`, shared across all five demos.

## Tests

```sh
python3 -m unittest -v
```

## License

MIT
