from .tags import *
from .tempy import Content, Css, render_template, TagAttrs, TempyREPR, Escaped

__version__ = '0.5.4'
VERSION = tuple(map(int, __version__.split('.')))
