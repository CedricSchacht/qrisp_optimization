"""Generate one API reference page per source file of the package.

Run by the ``gen-files`` plugin on every docs build; the pages only exist in the build,
not in ``docs/``.
"""

from pathlib import Path

import mkdocs_gen_files

PACKAGE = "qrisp_optimization"

nav = mkdocs_gen_files.Nav()
root = Path(__file__).parent.parent
# collected first and sorted by nav position, so the grouped requirements section is
# placed alphabetically instead of where its first module is found
entries: list[tuple[tuple[str, ...], str]] = []

for path in sorted((root / PACKAGE).rglob("*.py")):
    parts = path.relative_to(root).with_suffix("").parts
    doc_path = path.relative_to(root / PACKAGE).with_suffix(".md")

    if parts[-1] == "__init__":
        # a package is documented on the index page of its folder
        parts = parts[:-1]
        doc_path = doc_path.with_name("index.md")
    elif parts[-1].startswith("_"):
        continue

    # the top-level package is the landing page of the API reference
    nav_parts = parts[1:] or ("Overview",)
    if parts[-1].endswith("_requirements"):
        # group the requirement interfaces in the docs, while the modules stay top-level
        nav_parts = ("requirements", *nav_parts)
        doc_path = Path("requirements", doc_path)
    entries.append((nav_parts, doc_path.as_posix()))

    with mkdocs_gen_files.open(Path("reference", doc_path), "w") as fd:
        fd.write(f"::: {'.'.join(parts)}\n")

    mkdocs_gen_files.set_edit_path(Path("reference", doc_path), path.relative_to(root))

for nav_parts, doc in sorted(entries):
    nav[nav_parts] = doc

with mkdocs_gen_files.open("reference/SUMMARY.md", "w") as nav_file:
    nav_file.writelines(nav.build_literate_nav())
