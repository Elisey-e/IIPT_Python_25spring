master_doc = 'Index'

extensions = [
    'myst_parser',
    'sphinx_rtd_theme',
    'autodoc2',
    'sphinx_click',
    'matplotlib.sphinxext.plot_directive'
]
project = 'Image Interpolation Visualisation'

html_theme = 'furo'
html_logo = "source/_static/m31.png"

autodoc2_packages = [
    "../models",
]

myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "dollarmath",
]

source_suffix = {
    '.md': 'markdown',
}

autodoc2_render_plugin = "myst"
autosummary_generate = True