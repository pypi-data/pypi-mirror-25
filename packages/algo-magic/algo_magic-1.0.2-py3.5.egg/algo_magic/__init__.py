import sys

__version__ = '1.0.2'

if sys.version_info >= (3, 0):
    from algo_magic.algo_magic import *
else:
    from algo_magic import *

__all__ = ['algo_magic']
