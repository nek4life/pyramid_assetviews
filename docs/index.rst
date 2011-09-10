.. pyramid_assetviews documentation master file, created by
   sphinx-quickstart on Fri Sep  9 20:29:23 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

==================
pyramid_assetviews
==================

Installation
============

Install using ``easy_install`` or ``pip``

.. code-block:: text

   $ easy_install pyramid_assetviews


Overview
========

pyramid_assetviews is a small module that allows you to add Root-Relative 
views to your project. This enables you to serve assets that need to be
accessed from the root of your domain such as ``robots.txt`` or ``favicon.ico``
without having to setup a static media server such as nginx or lighttpd.
(Although in all fairness it's probably **not** preferable to serve static
media from your application and rather use a static media server instead.)

Usage
=====

To use pyramid_assetviews you simply include it in your applications config
like so:

.. code-block:: python
   :linenos:
   
   def main(global_config, **settings):
       config = Configurator(settings=settings)
       config.include("pyramid_assetviews")

Adding this to your Pyramid config will add the ``add_asset_views`` directive
to the config object.  Static assets may subsequently be added to your config
by using this new directive.  For example:

.. code-block:: python
   :linenos:
   
   def main(global_config, **settings):
       config = Configurator(settings=settings)
       config.include("pyramid_assetviews")
       
       # Adding your Root-Relative asset
       config.add_asset_views("my_module:static", 'robots.txt', 'favicon.ico')
       
       # Adding assets using argument expansion
       filenames = ['robots.txt', 'humans.txt', 'crossdomain.xml', 'favicon.ico']
       config.add_asset_views("my_module:static", *filenames)
       
The first argument uses the pyramid
`asset specification <https://pylonsproject.org/projects/pyramid/dev/narr/assets.html#understanding-asset-specifications>`_
to derive the location of the static files that will be served from the root
of the application.  The second argument ``*args`` takes unlimited filename arguments.