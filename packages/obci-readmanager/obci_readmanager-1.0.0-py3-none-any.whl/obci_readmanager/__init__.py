
from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

from ._version import get_versions
__revision__ = get_versions()['full-revisionid']
del get_versions

from .debug import install_debug_handler
install_debug_handler()
del install_debug_handler
