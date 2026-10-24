# skill-registry-lint

A linter that checks every `[[skill:name]]` reference and alias in a skill library resolves to a real skill.

**This is a scripted demo.** It represents the governance process I use in Palladium, my own agent framework. It is not a sample or excerpt of that system, and no Palladium code or data is in it.

- Live page: https://demos.obviouslogic.ai/skill-registry-lint/
- Source: https://github.com/obviouslogic-ai/skill-registry-lint

## How it fits Palladium governance

Palladium agents work from a shared library of skills, and renamed skills keep aliases. A reference that points nowhere fails quietly, so the library gets linted. This repo acts that out on a tiny `example/` library.

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

The page fits one screen. Press **Run the lint**: the reference graph draws in, broken references turn red, two scripted fixes are applied and the lint runs again clean. Press **Replay** to run it again. The explanation sits behind **About this demo** in the corner. Add `?fast=1` to skip the pauses.

The page runs this repo's real Python in the browser through Pyodide, so what you click is the same code the tests cover. Styling comes from `web/kit/`, shared across all five demos.

## Tests

```sh
python3 -m unittest -v
```

## License

MIT
