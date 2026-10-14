"""MkDocs hook that fixes links in notebook pages rendered by ``mkdocs-jupyter``.

Notebook markdown cells are rendered by nbconvert instead of Python-Markdown, so neither
autorefs cross-references (``[title][identifier]``) nor links to other pages
(``other.ipynb``, ``page.md``) are processed. This hook rewrites both in the rendered HTML:

- ``[title][identifier]`` becomes an ``<autoref>`` element, which the autorefs plugin
  resolves later (in ``on_env``) like any other cross-reference,
- ``href="other.ipynb"`` and ``href="page.md"`` are rewritten to the URL of the built page.
"""

import posixpath
import re

from mkdocs.structure.files import Files
from mkdocs.structure.pages import Page

# identifiers must be dotted paths (e.g. qrisp_optimization.QAOA), so that indexing
# such as x[i][j] in rendered outputs is never mistaken for a cross-reference
AUTOREF_RE = re.compile(r"\[([^\[\]]+?)\]\[([A-Za-z_]\w*(?:\.\w+)+)\]")
PAGE_HREF_RE = re.compile(r'href="(?![a-z]+:|/|#)([^"#]+\.(?:ipynb|md))(#[^"]*)?"')


def on_page_content(html: str, page: Page, files: Files, **kwargs: object) -> str:
    """Rewrite cross-references and notebook links of a notebook page."""
    if not page.file.src_uri.endswith(".ipynb"):
        return html

    html = AUTOREF_RE.sub(r'<autoref identifier="\2">\1</autoref>', html)

    def page_url(match: re.Match[str]) -> str:
        target = posixpath.normpath(posixpath.join(posixpath.dirname(page.file.src_uri), match[1]))
        file = files.get_file_from_path(target)
        if file is None:
            return match[0]
        return f'href="{file.url_relative_to(page.file)}{match[2] or ""}"'

    return PAGE_HREF_RE.sub(page_url, html)
