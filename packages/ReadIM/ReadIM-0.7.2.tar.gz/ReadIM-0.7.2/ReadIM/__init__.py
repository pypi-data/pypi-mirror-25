"""
ReadIM: A fast DaVis8 file reader and writer for Python
=======================================================

Documentation is available in the docstrings.

Contents
--------
ReadIM is a wrapper for for C-code provided by LaVision as the core
functionality. Additional functions are provided to load array data into memory
with access to data as numpy arrays and attributes as dictionaires.
"""
from __future__ import division, print_function, absolute_import

from . import extra
from . import core
# collect buffer fommats together
BUFFER_FORMATS = {}
for s in dir(core):
    if s.find('BUFFER_FORMAT') == 0:
        BUFFER_FORMATS[getattr(core, s)] = s

# collect error codes
ERROR_CODES = {}
for s in dir(core):
    if s.find('IMREAD_ERR') == 0:
        ERROR_CODES[getattr(core,s)] = s

del(s)
from .core import   (BufferType, BufferScaleType, AttributeList,
                    CreateBuffer, DestroyBuffer, DestroyAttributeList,
                    ReadIM7, WriteIM7, GetVectorComponents, SetBufferScale,
                    SetAttribute)

from .extra import *