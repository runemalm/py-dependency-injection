# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
from datetime import date
from importlib.metadata import PackageNotFoundError, version as pkg_version

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC = os.path.join(ROOT, "src")
sys.path.insert(0, SRC)


# The main module
root_doc = "index"


# -- Project information -----------------------------------------------------

project = "py-dependency-injection"
author = "David Runemalm"
copyright = f"{date.today().year}, {author}"

# Try to read the installed package version; fall back for local builds
try:
    release = pkg_version("py-dependency-injection")
except PackageNotFoundError:
    # Fallback: read from source without importing the package
    _ver_file = os.path.join(SRC, "dependency_injection", "version.py")
    _ver = "0.0.0-dev"
    try:
        with open(_ver_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip().startswith("__version__"):
                    _ver = line.split("=", 1)[1].strip().strip("\"'")
                    break
    except OSError:
        pass
    release = _ver

version = release.split("-")[0]


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",  # generate API from docstrings
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.autosummary",  # summary tables + per-object pages
    "sphinx.ext.napoleon",  # Google/NumPy docstrings
    "sphinx_autodoc_typehints",  # display type hints nicely
    "sphinx.ext.intersphinx",  # cross-link to Python stdlib, etc.
    "sphinx.ext.linkcode",  # "view source" links
    "sphinx.ext.doctest",  # run code in docs if you want
    "sphinx_copybutton",
    "sphinx_inline_tabs",
]

# --- Theme ---
html_theme = "sphinx_rtd_theme"

# Optional RTD theme polish
# html_theme_options = {
#    "collapse_navigation": True,
#    "navigation_depth": 3,
#    "style_external_links": True,
# }

html_context = {
    "display_github": False,  # Optional: only needed if you're showing GitHub links
    "display_version": True,  # ✅ Enable version display manually
    "version": version,  # pulled from your __version__
    "release": release,
}

html_css_files = ["custom.css"]

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# --- Autosectionlabel behavior ---
autosectionlabel_prefix_document = True

# --- Autodoc / Autosummary behavior ---
autosummary_generate = True
# If you re-export public API from __init__.py, uncomment:
# autosummary_imported_members = True
autodoc_default_options = {
    "members": True,
    "undoc-members": False,
    "inherited-members": True,
    "show-inheritance": True,
}
autodoc_member_order = "bysource"
autodoc_preserve_defaults = True  # show default arg values as written

# sphinx-autodoc-typehints tuning
typehints_fully_qualified = False
always_document_param_types = True
set_type_checking_flag = True
simplify_optional_unions = True
typehints_use_rtype = False

# --- Don’t explode when optional deps aren’t installed during docs build ---
# If your package has optional imports, list them here to mock:
autodoc_mock_imports = [
    # "fastapi", "some_heavy_provider",
]

# --- Copybutton behaviour -------------------------------------------------
copybutton_prompt_text = r">>> |\.\.\. |\$ |In \[\d+\]: |Out\[\d+\]: "
copybutton_prompt_is_regexp = True

# --- Napoleon (Google style recommended) ---
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_use_param = True
napoleon_use_rtype = False  # keep return type in signature from hints
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_examples = True

# -- General configuration ---------------------------------------------------
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}

# --- Strictness (great for CI; relax locally if needed) ---
nitpicky = True  # warn on broken references
nitpick_ignore = [
    # Example if a third-party type isn’t resolvable:
    # ("py:class", "SomeExternalType"),
]
# In CI, also run sphinx-build with -W to turn warnings into errors.

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [
    "_build",
    "**/site-packages/**",
    "Thumbs.db",
    ".DS_Store",
    "build",
    ".git",
    "examples",
    "scratch",
    "tests",
]

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"

# A list of ignored prefixes for module index sorting.
# modindex_common_prefix = []


# -- Linkcode: map objects to GitHub -----------------------------------------
def linkcode_resolve(domain, info):
    if domain != "py" or not info.get("module"):
        return None
    import importlib
    import pathlib
    import inspect as _inspect

    try:
        mod = importlib.import_module(info["module"])
    except Exception:
        return None

    obj = mod
    for part in info["fullname"].split("."):
        obj = getattr(obj, part, None)
        if obj is None:
            return None

    try:
        fn = _inspect.getsourcefile(obj) or _inspect.getfile(obj)
        source, lineno = _inspect.getsourcelines(obj)
    except Exception:
        return None

    fn = pathlib.Path(fn).resolve()
    try:
        relpath = fn.relative_to(SRC)
    except ValueError:
        return None

    # Prefer commit/tag if present; fall back to branch-ish
    ref = (
        os.environ.get("READTHEDOCS_GIT_IDENTIFIER")  # exact commit or tag
        or os.environ.get("READTHEDOCS_VERSION")  # 'latest'/'stable'/branch
        or "master"
    )

    start, end = lineno, lineno + len(source) - 1
    return (
        "https://github.com/runemalm/py-dependency-injection/"
        f"blob/{ref}/src/{relpath}#L{start}-L{end}"
    )
