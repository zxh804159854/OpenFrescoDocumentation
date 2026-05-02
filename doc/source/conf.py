# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'OpenFrescoDocumentation'
copyright = '2026, ZXH'
author = 'ZXH'
release = '0.0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['myst_parser', 'sphinx.ext.mathjax'] #md文档，数学公式

myst_enable_extensions = [
    "dollarmath",
    "amsmath",
]#dollarmath解析$x$和$$xxx$$,amsmath解析latex语法。

numfig = True   #开启md的图编号

templates_path = ['_templates']
exclude_patterns = []

language = 'zh_CN'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme" #更改主题
html_static_path = ['_static']
