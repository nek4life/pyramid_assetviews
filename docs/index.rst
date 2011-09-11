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
       
       # Adding a single Root-Relative asset
       config.add_asset_views("my_module:static", 'robots.txt')
       
       # Adding multiple assets using the filenames argument.
       filenames = ['robots.txt', 'humans.txt', 'crossdomain.xml', 'favicon.ico']
       config.add_asset_views("my_module:static", filenames=filenames)
         
Optionally you may use the ``http_cache`` argument to specify the time in seconds
that the file should remained cached.  If you need to specify cache settings
per file you will have to call ``add_asset_views`` multiple times instead of
using the ``filenames`` argument.

.. code-block:: python
   :linenos:
   
   def main(global_config, **settings):
       config = Configurator(settings=settings)
       config.include("pyramid_assetviews")
       
       # Adding your Root-Relative asset with http_cache
       config.add_asset_views("my_module:static", 'robots.txt', http_cache=5000)
       config.add_asset_views("my_module:static", 'humans.txt', http_cache=3000)
       
       # All files in the filenames list would have the same http_cache value
       filenames = ['robots.txt', 'humans.txt', 'crossdomain.xml', 'favicon.ico']
       config.add_asset_views("my_module:static", filenames=filenames, http_cache=5000)

