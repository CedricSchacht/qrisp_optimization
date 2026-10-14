# Development

## Setup

The project uses [uv](https://docs.astral.sh/uv/). Install the package together with all
development tools:

```bash
uv sync --all-groups
```

## Checks

Run all of these before committing; they must pass without errors.

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

## Docstrings

Docstrings follow the [numpy convention](https://numpydoc.readthedocs.io/en/latest/format.html),
which Ruff checks. They are rendered into the [API reference](api/index.md) by
[mkdocstrings](https://mkdocstrings.github.io/), so write them in **Markdown**, not
reStructuredText:

- Cross-reference other objects with their full import path:
  ``[`QAOA`][qrisp_optimization.QAOA]``, not ``:class:`QAOA` ``.
- Keep the one-line summary free of long links; put references in the body instead.

## Documentation

The docs are built with [ProperDocs](https://pypi.org/project/properdocs/) and configured in
`properdocs.yml`. Pages live in `docs/`.

```bash
uv run properdocs serve           # live preview at http://127.0.0.1:8000
uv run properdocs build --strict  # fails on broken links or other warnings
```

- **API reference**: new public classes and functions are added to the matching page in
  `docs/api/` with a `::: qrisp_optimization.<path>` line.
- **Guides**: Jupyter notebooks in `docs/guides/`, listed under `Guides` in the `nav` of
  `properdocs.yml`. Notebooks are not executed during the build, so run them and save the
  outputs before committing.
