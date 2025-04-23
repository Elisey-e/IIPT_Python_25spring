master_doc = 'Index'

extensions = [
    'myst_parser',
    'sphinx_rtd_theme',
    'autodoc2',
    'sphinx_click',
    'matplotlib.sphinxext.plot_directive'
]

html_theme = 'furo'

autodoc2_packages = [
    "../myproject",
]

myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "dollarmath",
]

source_suffix = {
    '.md': 'markdown',
}
