from pyramid import testing
import unittest

class TestAssetViewConfig(unittest.TestCase):

    def setUp(self):
        self.request = testing.DummyRequest()
        self.config = testing.setUp(request=self.request)
        self.request.registry = self.config.registry
        import os
        here = os.path.abspath(os.path.dirname(__file__))
        self.test_assets = os.path.join(here, 'test_assets')

    def tearDown(self):
        testing.tearDown()
        del self.config

    def test_config(self):
        self.assertNotEqual(self.config, None)

    def test_directive_added(self):
        self.config.include("pyramid_assetviews")
        self.assertNotEqual(self.config.add_asset_views, None)

class TestAssetView(unittest.TestCase):

    def setUp(self):
        self.request = testing.DummyRequest()
        self.config = testing.setUp(request=self.request)
        self.request.registry = self.config.registry
        import os
        here = os.path.abspath(os.path.dirname(__file__))
        self.test_assets = os.path.join(here, 'test_assets')

    def tearDown(self):
        testing.tearDown()
        del self.config

    def test_asset_view_factory(self):
        from pyramid_assetviews import asset_view_factory
        asset_view = asset_view_factory("body", "image/x-icon")
        response = asset_view("context", self.request)
        self.assertEqual(response.app_iter, ['body'])
        self.assertEqual(response.content_type, 'image/x-icon')

    def test_add_asset_views(self):
        from pyramid_assetviews import add_asset_views
        asset_spec = 'pyramid_assetviews:test_assets'
        filenames = ['favicon.ico', 'crossdomain.xml', 'robots.txt']
        add_asset_views(self.config, asset_spec, *filenames)

    def test_add_asset_views_with_bad_mimetype(self):
        from pyramid_assetviews import add_asset_views
        asset_spec = 'pyramid_assetviews:test_assets'
        filenames = ['badmimetype.xyz']
        add_asset_views(self.config, asset_spec, *filenames)

    def test_simple_response(self):
        from pyramid_assetviews import SimpleResponse
        response = SimpleResponse('body', 'image/x-icon')
        self.assertEqual(response.content_type, 'image/x-icon')
        self.assertEqual(response.app_iter, ['body'])
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.headerlist, [('Content-Type', 'image/x-icon'),
                                               ('Content-Length', '4')])
