# https://www.sphinx-doc.org/en/master/usage/configuration.html

import alabaster

project = "library"
copyright = "2019, Matt VanEseltine"
author = "Matt VanEseltine"

# -- General configuration ---------------------------------------------------

extensions = []

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

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
# not completely unusable:
# - basic
# - classic
# - sphinxdoc
html_theme_path = [alabaster.get_path()]
extensions += ["alabaster"]
html_theme = "alabaster"

# A Windows icon file (.ico) 16x16 or 32x32 pixels large.
html_favicon = "./static/favicon.ico"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_theme_options = {
    "fixed_sidebar": True,
    # "logo": "logo.png",
    "logo_name": True,
    "canonical_url": "https://misterdoubt.com",
    "logo_text_align": "left",
    "description": "somewhere between a personal wiki and a blog",
    "show_powered_by": True,
    "show_relbars": True,
    "show_related": False,
}
html_show_sphinx = False
html_title = "library"
