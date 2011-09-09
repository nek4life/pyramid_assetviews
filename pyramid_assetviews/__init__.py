import os
import mimetypes
from pyramid.asset import abspath_from_asset_spec
from pyramid.interfaces import IResponse
from zope.interface import implements

class SimpleResponse(object):
    """ Slightly faster than webob.Response """
    implements(IResponse)
    def __init__(self, body, content_type):
        self.status = '200 OK'
        self.app_iter = [body]
        self.content_type = content_type
        self.headerlist = [('Content-Type', content_type),
                           ('Content-Length', str(len(body)))]

    def __call__(self, environ, start_response):
        start_response(self.status, self.headerlist)
        return self.app_iter

def asset_view_factory(body, content_type):
    response = SimpleResponse(body, content_type)
    def asset_view(context, request):
        return response
    return asset_view

def add_asset_views(config, spec, *names):
    path = abspath_from_asset_spec(spec)
    for name in names:
        content_type = mimetypes.guess_type(name, strict=False)[0]
        if content_type is None:
            content_type = 'application/octet-stream'
        filename = os.path.join(path, name)
        body = open(filename, 'rb').read()
        config.add_view(asset_view_factory(body, content_type), name=name)

def includeme(config):
    config.add_directive('add_asset_views', add_asset_views)
