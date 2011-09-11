import unittest
from pyramid import testing

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
        self.assertTrue(self.config is not None)

    def test_directive_added(self):
        self.config.include("pyramid_assetviews")
        self.assertTrue(self.config.add_asset_views is not None)


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

    def test_no_filenames_exception(self):
        from pyramid_assetviews import add_asset_views
        from pyramid_assetviews import NoFilenamesProvided
        with self.assertRaises(NoFilenamesProvided):
            add_asset_views(self.config, 'pyramid_assetviews:test_assets')

    def test_asset_view_factory(self):
        from pyramid_assetviews import asset_view_factory
        asset_view = asset_view_factory("body", "image/x-icon", 124432, http_cache=500)
        response = asset_view("context", self.request)
        self.assertEqual(response.app_iter, ['body'])
        self.assertEqual(response.content_type, 'image/x-icon')
        self.assertTrue(response.last_modified is not None)
        self.assertTrue(response.expires is not None)
        self.assertTrue(response.cache_control.max_age, 500)

    def test_add_asset_views(self):
        from pyramid_assetviews import add_asset_views
        asset_spec = 'pyramid_assetviews:test_assets'
        filenames = ['favicon.ico', 'crossdomain.xml', 'robots.txt']
        add_asset_views(self.config, asset_spec, filenames=filenames)
        add_asset_views(self.config, asset_spec, 'robots.txt')
        add_asset_views(self.config, asset_spec, 'robots.txt', http_cache=500)

    def test_add_asset_views_with_no_mimetype(self):
        from pyramid_assetviews import add_asset_views
        asset_spec = 'pyramid_assetviews:test_assets'
        filenames = ['nomimetype']
        add_asset_views(self.config, asset_spec, filenames=filenames)
