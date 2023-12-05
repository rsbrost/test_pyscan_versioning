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
sys.path.insert(0, os.path.abspath('../..'))


# -- Project information -----------------------------------------------------

project = 'pyscan'
copyright = '2023, Andrew Mounce'
author = 'Andrew Mounce'

# The full version, including alpha/beta/rc tags
release = '0.0.0'

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
        'sphinx.ext.autodoc',
        'sphinx.ext.coverage',
        'numpydoc',
]

numpydoc_show_inherited_class_members = False
numpydoc_class_members_toctree = False

autodoc_typehints = "none"
autodoc_docstring_signature = True
autodoc_default_options = {'members': None}


# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'mpl_sphinx_theme'
# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

html_theme_options = {
    "logo": { #"link": "https://matplotlib.org/stable/",
             "image_light": "_static/pyscan logo v3.svg",
             "image_dark": "_static/pyscan logo v3.svg",
        },
    # collapse_navigation in pydata-sphinx-theme is slow, so skipped for local
    # and CI builds https://github.com/pydata/pydata-sphinx-theme/pull/386
    # "collapse_navigation": not is_release_build,
    "show_prev_next": False,
    # Determines the type of links produced in the navigation header:
    # - absolute: Links point to the URL https://matplotlib.org/...
    # - server-stable: Links point to top-level of the server /stable/...
    # - internal: Links point to the internal files as expanded by the `pathto`
    #   template function in Sphinx.
    "navbar_links": "absolute",
}
