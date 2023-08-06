# -*- coding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals, print_function

from modelchemy import REQUEST_KEY
from modelchemy import dbs
from modelchemy.requests import RequestSessionFactory


class RequestInjectorMiddleware(object):
    def __init__(self, get_response=None):
        self.get_response = get_response
        super(RequestInjectorMiddleware, self).__init__()

    def __call__(self, request):
        self.process_request(request)
        response = self.get_response(request)
        response = self.process_response(request, response)
        return response

    @staticmethod
    def process_request(request):
        factory = RequestSessionFactory()

        [factory.register(key, lambda: dbs[key].Session(), dbs[key].metadata)
         for
         key in dbs.keys]

        setattr(request, REQUEST_KEY, factory)

    @staticmethod
    def process_response(request, response):
        if hasattr(request, REQUEST_KEY):
            getattr(request, REQUEST_KEY).close()
        return response
