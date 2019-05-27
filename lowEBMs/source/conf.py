# -*- coding: utf-8 -*-
#
# Configuration file for the Sphinx documentation builder.
#
# This file does only contain a selection of the most common options. For a
# full list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
sys.path.insert(0, os.path.abspath('../'))
sys.path.insert(0, os.path.abspath('../../'))


# -- Project information -----------------------------------------------------

project = 'Low-dimensional Energybalance models'
copyright = '2019, benni'
author = 'benni'

# The short X.Y version
version = ''
# The full version, including alpha/beta/rc tags
release = ''


# -- General configuration ---------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.autosectionlabel',
    'sphinx.ext.viewcode',
    'sphinx.ext.mathjax'
]
autosectionlabel_prefix_document = True

#autodoc_default_flags = ['members']
autosummary_generate = True

autodoc_docstring_signature = False

autodoc_mock_imports = ['matplotlib',
          'numpy',
          'netCDF4',
          'climlab',
          'xarray',
          'attrdict',
          'scipy'
]

language = 'en'
templates_path = ['_templates']
source_suffix = '.rst'
exclude_patterns = []

master_doc = 'index'
pygments_style = 'default'

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_logo = '/_static/logos_combined.jpg'


htmlhelp_basename = 'docdoc'


# -- Options for LaTeX output ------------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',

    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

latex_documents = [
    (master_doc, 'doc.tex', 'doc Documentation',
     'benni', 'manual'),
]

man_pages = [
    (master_doc, 'doc', 'doc Documentation',
     [author], 1)
]

texinfo_documents = [
    (master_doc, 'doc', 'doc Documentation',
     author, 'doc', 'One line description of project.',
     'Miscellaneous'),
]


# -- Options for Epub output -------------------------------------------------

# Bibliographic Dublin Core info.
epub_title = project

# The unique identifier of the text. This can be a ISBN number
# or the project homepage.
#
# epub_identifier = ''

# A unique identification for the text.
#
# epub_uid = ''

# A list of files that should not be packed into the epub file.
epub_exclude_files = ['search.html']

