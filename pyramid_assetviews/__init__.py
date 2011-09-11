import os
import mimetypes
from webob import Response
from pyramid.asset import abspath_from_asset_spec

class NoFilenamesProvided(Exception):
    pass

def asset_view_factory(body, content_type, last_modified, http_cache=None):
    """ Returns an asset_view function that returns a SimpleResponse object"""
    response = Response()
    response.body = body
    response.content_type = content_type
    response.last_modified = last_modified
    response.cache_expires = http_cache
    def asset_view(context, request):
        return response
    return asset_view

def add_asset_views(config, spec, filename=None, filenames=None, http_cache=None):
    """ A pyramid directive that takes an asset spec and a file name or list of
    filenames and adds them to the pyramid config via the `add_view` function.

    These files added by this directive will be served relative to the Root
    of the application.  For Example:

    config.add_asset_views("mymodule:static", "favicon.ico")

    Alternatively you could use argument expansion with longer file lists:

    filenames = ['favicon.ico', 'robots.txt', 'humans.txt', 'crossdomain.xml']
    config.add_asset_views("mymodule:static", filenames=filenames)

    favicon.ico and robots.txt located in mymodule/static/ will now be served
    from /favicon.ico and /robots.txt respectively.

    Optionally the http_cache argument may be set with a number that represents
    a length of time in seconds.  For Example:

    config.add_asset_views("mymodule:static", "favicon.ico", http_cache=50000)

    Large files are not meant to be served this way as the current
    implementation reads the entire file into memory before generating the
    response object.  The main purpose of this module is to include assets
    that must be served from the root of the domain such as favicon.ico,
    robots.txt, and crossdomain.xml.
    """
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
                               http_cache=http_cache), name=name)

def includeme(config):
    """ Adds the add_asset_views directive into a pyramid applications config
    """
    config.add_directive('add_asset_views', add_asset_views)
