# Copyright (c) 2017-2018. See LICENSE for details.

from ._version import __version__ as _incremental_version


__all__ = (
    "__version__",
)


# Make it a str, for backwards compatibility
__version__ = _incremental_version.base()
