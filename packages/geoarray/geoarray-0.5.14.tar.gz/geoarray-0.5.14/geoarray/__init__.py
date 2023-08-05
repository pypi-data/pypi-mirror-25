# -*- coding: utf-8 -*-

import os
if 'MPLBACKEND' not in os.environ:
    os.environ['MPLBACKEND'] = 'Agg'

from .baseclasses import GeoArray
from .masks import BadDataMask
from .masks import NoDataMask
from .masks import CloudMask


__author__ = """Daniel Scheffler"""
__email__ = 'danschef@gfz-potsdam.de'
__version__ = '0.5.14'
__versionalias__ = 'v20170911.03'
__all__ = ['GeoArray',
           'BadDataMask',
           'NoDataMask',
           'CloudMask'
           ]
