=========
txrequest
=========

.. image:: https://travis-ci.org/wsanchez/txrequest.svg?branch=master
    :target: http://travis-ci.org/wsanchez/txrequest
    :alt: Build Status
.. image:: https://codecov.io/github/wsanchez/txrequest/coverage.svg?branch=master
    :target: https://codecov.io/github/wsanchez/txrequest?branch=master
    :alt: Code Coverage
.. image:: https://img.shields.io/pypi/pyversions/txrequest.svg
    :target: https://pypi.python.org/pypi/txrequest
    :alt: Python Version Compatibility

``txrequest`` is a library containing an HTTP Request object API for Twisted, meant to replace the `IRequest <http://twistedmatrix.com/documents/current/api/twisted.web.iweb.IRequest.html>`_ interface and implementations in ``twisted.web``.

``txrequest`` is not an attempt at a an async version of ``requests``.  For that, see `treq <https://github.com/twisted/treq>`_.
