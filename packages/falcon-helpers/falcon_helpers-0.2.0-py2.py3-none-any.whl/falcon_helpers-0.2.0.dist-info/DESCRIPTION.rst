.. default-role:: code
.. role:: python(code)
  :language: python

==============
Falcon Helpers
==============

A number of helpful utilities to make working with Falcon Framework a breeze.


Quickstart
----------

.. code:: sh

  $ pip install falcon-helpers


.. code::

  import falcon
  import falcon_helpers

  api = falcon.API(
    middlewares=[
      falcon_helpers.middlewares.StaticsMiddleware()
    ]
  )


0.2.0 - 2017-09-23
==================
* Release the Package and update the source location

0.1.0 - 2017-08-22
==================

* Added StaticsMiddleware


