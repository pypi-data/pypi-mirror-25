import sys
if sys.version_info[0] == 3:
    from kyew.kyew import Kyew
else:
    from kyew import Kyew

__version__ = '0.1.3'
VERSION = tuple(map(int, __version__.split('.')))

__all__ = ['Kyew']
