import os
import mimetypes
from webob import Response
from pyramid.asset import abspath_from_asset_spec

class NoFilenamesProvided(Exception):
    pass

def asset_view_factory(body, content_type, last_modified, cache_max_age=None):
    """ Returns an asset_view function that returns a SimpleResponse object"""
    response = Response()
    response.body = body
    response.content_type = content_type
    response.last_modified = last_modified
    response.cache_expires = cache_max_age
    def asset_view(context, request):
        return response
    return asset_view

def add_asset_views(
            config, spec, filename=None, filenames=None, cache_max_age=None):

    if filename is None and filenames is None:
        raise NoFilenamesProvided

    path = abspath_from_asset_spec(spec)

    if not filenames:
        filenames = []

    if filename:
        filenames.append(filename)

    for name in filenames:
        content_type = mimetypes.guess_type(name, strict=False)[0]
        if content_type is None:
            content_type = 'application/octet-stream'
        filename = os.path.join(path, name)
        body = open(filename, 'rb').read()
        last_modified = os.stat(filename).st_mtime
        config.add_view(asset_view_factory(body, content_type, last_modified,
                               cache_max_age=cache_max_age), name=name)

def includeme(config):
    """ Adds the add_asset_views directive into a pyramid applications config
    """
    config.add_directive('add_asset_views', add_asset_views)
