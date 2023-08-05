from __future__ import (division, print_function, absolute_import, unicode_literals)
from . import compatibility
from . import convenience
from . import dtypes
from . import geo
from . import io
from . import numeric
from . import similarity
from . import web

__version__ = '0.5.0'
__versionalias__ = '20170911_03'
__author__ = 'Daniel Scheffler'

# Validate GDAL version
try:
    import gdal
    import gdalnumeric
except ImportError:
    from osgeo import gdal
    from osgeo import gdalnumeric

try:
    getattr(gdal, 'Warp')
    getattr(gdal, 'Translate')
    getattr(gdalnumeric, 'OpenNumPyArray')
except AttributeError:
    import warnings
    warnings.warn("Your GDAL version is too old to support all functionalities of the 'py_tools_ds' package. "
                  "Please update GDAL!")
del gdal, gdalnumeric
