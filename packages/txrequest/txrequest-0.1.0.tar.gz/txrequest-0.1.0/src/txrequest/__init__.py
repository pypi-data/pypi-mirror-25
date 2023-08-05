# Copyright (c) 2017-2018. See LICENSE for details.

from ._headers import FrozenHTTPHeaders, IHTTPHeaders, MutableHTTPHeaders
from ._request import FrozenHTTPRequest, IHTTPRequest
from ._version import __version__ as _incremental_version


__all__ = (
    "__version__",
    "FrozenHTTPHeaders",
    "FrozenHTTPRequest",
    "HTTPHeadersWrappingHeaders",
    "IHTTPHeaders",
    "IHTTPRequest",
    "MutableHTTPHeaders",
)


# Use a string, per PEP 8, PEP 386
__version__ = _incremental_version.base()
