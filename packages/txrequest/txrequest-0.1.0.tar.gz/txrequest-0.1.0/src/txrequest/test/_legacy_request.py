# This file is copied from:
# https://github.com/twisted/klein/blob/master/src/klein/test/test_resource.py
#
# Copyright (c) 2011-2018, Klein Contributors; see:
# https://github.com/twisted/klein/blob/master/LICENSE
#
# The code here is a good primer as to why we have implemented a new API.
# Creating a request object for testing should not be this hard.

from io import BytesIO

from mock import Mock

from six.moves.urllib.parse import parse_qs

from twisted.web.http_headers import Headers
from twisted.web.server import Request, Site
from twisted.web.test.test_web import DummyChannel


def requestMock(path, method=b"GET", host=b"localhost", port=8080,
                isSecure=False, body=None, headers=None):
    if not headers:
        headers = {}

    if not body:
        body = b''

    path, qpath = (path.split(b"?", 1) + [b""])[:2]

    request = Request(DummyChannel(), False)
    request.site = Mock(Site)
    request.gotLength(len(body))
    request.content = BytesIO()
    request.content.write(body)
    request.content.seek(0)
    request.args = parse_qs(qpath)
    request.requestHeaders = Headers(headers)
    request.setHost(host, port, isSecure)
    request.uri = path
    request.prepath = []
    request.postpath = path.split(b'/')[1:]
    request.method = method
    request.clientproto = b'HTTP/1.1'

    request.setHeader = Mock(wraps=request.setHeader)
    request.setResponseCode = Mock(wraps=request.setResponseCode)

    request._written = BytesIO()
    request.finishCount = 0
    request.writeCount = 0

    def registerProducer(producer, streaming):
        request.producer = producer
        for _ in range(2):
            if request.producer:
                request.producer.resumeProducing()

    def unregisterProducer():
        request.producer = None

    def finish():
        request.finishCount += 1

        if not request.startedWriting:
            request.write(b'')

        if not request.finished:
            request.finished = True
            request._cleanup()

    def write(data):
        request.writeCount += 1
        request.startedWriting = True

        if not request.finished:
            request._written.write(data)
        else:
            raise RuntimeError('Request.write called on a request after '
                               'Request.finish was called.')

    def getWrittenData():
        return request._written.getvalue()

    request.finish = finish
    request.write = write
    request.getWrittenData = getWrittenData

    request.registerProducer = registerProducer
    request.unregisterProducer = unregisterProducer

    request.processingFailed = Mock(wraps=request.processingFailed)

    return request
