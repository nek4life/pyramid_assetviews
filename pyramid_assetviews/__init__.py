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
    """ Returns an asset_view function that returns a SimpleResponse object"""
    response = SimpleResponse(body, content_type)
    def asset_view(context, request):
        return response
    return asset_view

def add_asset_views(config, spec, *names):
    """ A pyramid directive that takes a asset spec and filename keywords
    and adds them to the pyramid config via the `add_view` function.

    These files added by this directive will be served relative to the Root
    of the application.  For Example:

    config.add_asset_views("mymodule:static", "favicon.ico", "robots.txt")

    Alternatively you could use argument expansion with longer file lists:

    filenames = ['favicon.ico', 'robots.txt', 'humans.txt', 'crossdomain.xml']
    config.add_asset_views("mymodule:static", *filenames)

    favicon.ico and robots.txt located in mymodule/static/ will now be served
    from /favicon.ico and /robots.txt respectively.

    Large files are not meant to be served this way as the current
    implementation reads the entire file into memory before generating the
    response object.  The main purpose of this module is to include assets
    that must be served from the root of the domain such as favicon.ico,
    robots.txt, and crossdomain.xml.
    """
    path = abspath_from_asset_spec(spec)
    for name in names:
        content_type = mimetypes.guess_type(name, strict=False)[0]
        if content_type is None:
            content_type = 'application/octet-stream'
        filename = os.path.join(path, name)
        body = open(filename, 'rb').read()
        config.add_view(asset_view_factory(body, content_type), name=name)

def includeme(config):
    """ Adds the add_asset_views directive into a pyramid applications config
    """
    config.add_directive('add_asset_views', add_asset_views)
