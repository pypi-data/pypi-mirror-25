"""Shay Palachy's personal common Python 3 utility functions and classes."""

# pylint: disable=W0614,W0401,C0413
# pylint: disable=W0611
# import utilp.classes as classes
# import utilp.constants as constants
# import utilp.contextmanagers as contextmanagers
import utilp.classes as classes
# import utilp.exceptions as exceptions
# import utilp.functions as functions
# import utilp.generators as generators
# import utilp.functional as functional
# import utilp.output as output
# import utilp.interface as interface

# cleaning the module's name space
for name in ['get_versions', '_version', 'name']:
    try:
        globals().pop(name)
    except KeyError:
        pass

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
