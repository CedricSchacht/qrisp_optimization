# Development

## Setup

The project uses [uv](https://docs.astral.sh/uv/). Install the package together with all
development tools:

```bash
uv sync --all-groups
```

## Checks

Run all checks and build the docs with:

```bash
scripts/check.sh         # only check
scripts/check.sh --fix   # format the code and apply automatic lint fixes first
```

Everything must pass before committing. The script runs these steps, which can also be run
individually:

```bash
uv run ruff format    # code formatting
uv run ruff check     # linting, import order, naming, docstrings
uv run mypy           # strict static type checking
uv run pytest         # tests in tests/
```

### Ruff

[Ruff](https://docs.astral.sh/ruff/) is used both as formatter and linter. It is configured
in `pyproject.toml` under `[tool.ruff]` (line length 100, target Python 3.14).

```bash
uv run ruff format          # reformat all files
uv run ruff format --check  # only report files that would be reformatted
uv run ruff check --fix     # fix lint issues that can be fixed automatically, e.g. import order
```

Notebooks are excluded from formatting and linting.

### Mypy

[Mypy](https://mypy.readthedocs.io/) runs in `strict` mode on `qrisp_optimization` and
`main.py` (see `[tool.mypy]` in `pyproject.toml`). Every function needs full type
annotations. Qrisp ships no type information, so its classes are typed as `Any`.

## Coding conventions

### Requirements files

The requirements interface of an algorithm lives in its own module named
`<algorithm-name>_requirements.py`, directly in `qrisp_optimization/`, next to the
algorithm's module `<algorithm-name>.py`:

| Algorithm module | Requirements module          | Requirements class       |
| ---------------- | ---------------------------- | ------------------------ |
| `qaoa.py`        | `qaoa_requirements.py`       | `QAOARequirements`       |
| `bruteforce.py`  | `bruteforce_requirements.py` | `BruteforceRequirements` |

- Name the class `<AlgorithmName>Requirements`.
- Several algorithms can share one requirements interface; [`LRQAOA`][qrisp_optimization.LRQAOA]
  uses `QAOARequirements` instead of defining its own.
- Interfaces shared by several requirements follow the same pattern, e.g.
  `cl_cost_requirements.py` for the classical cost function both interfaces build on.
- Re-export the class in `qrisp_optimization/__init__.py`.

The `_requirements` suffix is not just a naming convention: the API reference
generator groups every module ending in `_requirements` under the **requirements**
section. A requirements module with a different name ends up in the wrong place in the
docs.

## Docstrings

Docstrings follow the [numpy convention](https://numpydoc.readthedocs.io/en/latest/format.html),
which Ruff checks. They are rendered into the [API reference](reference/index.md) by
[mkdocstrings](https://mkdocstrings.github.io/), so write them in **Markdown**, not
reStructuredText:

- Cross-reference other objects with their import path:
  ``[`QAOA`][qrisp_optimization.QAOA]``, not ``:class:`QAOA` ``.
  Methods and attributes need the path of the module that defines them, e.g.
  ``[`ansatz`][qrisp_optimization.qaoa.QAOA.ansatz]``.
- Keep the one-line summary free of long links; put references in the body instead.

## Documentation

The docs are built with [ProperDocs](https://pypi.org/project/properdocs/) and configured in
`properdocs.yml`. Pages live in `docs/`.

```bash
uv run properdocs serve           # live preview at http://127.0.0.1:8000
uv run properdocs build --strict  # fails on broken links or other warnings
```

- **API reference**: generated on every build by `scripts/gen_ref_pages.py`, one page per
  source file of `qrisp_optimization`. New modules appear automatically; files starting
  with `_` (other than `__init__.py`) are skipped.
- **Guides**: Jupyter notebooks in `docs/guides/`, listed under `Guides` in the `nav` of
  `properdocs.yml`. Notebooks are not executed during the build, so run them and save the
  outputs before committing.
