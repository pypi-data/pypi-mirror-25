""" Pixelink Camera driver package initializer. """

from .pixelink_api import PixeLINK
from .pixelink_api import PxLapi
from .pixelink_api import PxLerror
# from .pixelink_streamer import PxLstreamer

__all__ = ['PxLapi', 'PixeLINK', 'PxLerror', 'PxLstreamer']

__pkgname__ = 'pixelink'
__desc__ = 'A Python driver for the PixeLINK camera'
__created__ = '12/02/2014'
__updated__ = '02/10/2017'
__author__ = 'Hans Smit, Danny Smith'
__email__ = 'Hans.Smit@esa.int, danny.smith@uq.edu.au'
__copyright_ = 'Copyright 2014, SCI-F, ESA'
__license__ = 'GNU GPL'
__version__ = '1.3.1'
