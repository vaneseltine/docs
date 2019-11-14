# https://www.sphinx-doc.org/en/master/usage/configuration.html

import alabaster

project = "consuetudinary"
copyright = "2019, Matt VanEseltine"
author = "Matt VanEseltine"

# -- General configuration ---------------------------------------------------

extensions = ["sphinx.ext.graphviz", "sphinx.ext.autosectionlabel"]

autosectionlabel_prefix_document = False

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["static"]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "__pycache__" ".git", ".nox", ".venv", ".vscode"]

# -- General extensions ------------------------------------------------------

extensions = ["sphinx.ext.graphviz", "sphinx.ext.autosectionlabel"]

autosectionlabel_prefix_document = False

# -- HTML output -------------------------------------------------------------

html_show_sphinx = False
html_show_sourcelink = False
html_show_copyright = False
html_title = "consuetudinary"

# A Windows icon file (.ico) 16x16 or 32x32 pixels large.
html_favicon = "./static/favicon.ico"

# not completely unusable: alabaster; basic; classic; sphinxdoc
html_theme_path = [alabaster.get_path()]
extensions += ["alabaster"]
html_theme = "alabaster"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_theme_options = {
    "fixed_sidebar": True,
    "logo": "logo.png",
    "logo_name": False,
    "canonical_url": "https://misterdoubt.com",
    "logo_text_align": "center",
    "description": (
        r"con·sue·tu·di·nar·y:<br>a book of customs, traditions, and principles."
    ),
    "show_powered_by": False,
    "show_relbars": True,
    "show_related": False,
}

# -- reStructuredText magic --------------------------------------------------

rst_prolog = """
.. highlight:: python
    :linenothreshold: 1
"""
