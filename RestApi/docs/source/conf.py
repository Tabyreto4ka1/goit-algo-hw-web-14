import sys
import os


sys.path.insert(0, os.path.abspath('../..'))
project = 'Rest Api'
copyright = '2026, Tabyret'
author = 'Tabyret'


extensions = [
    'sphinx.ext.autodoc',
]
templates_path = ['_templates']
exclude_patterns = []



html_theme = 'alabaster'
html_static_path = ['_static']
