=========
yamicache
=========


.. image:: https://img.shields.io/pypi/v/yamicache.svg
        :target: https://pypi.org/project/yamicache/
        :alt: Pypi Version

.. image:: https://img.shields.io/travis/mtik00/yamicache.svg
        :target: https://travis-ci.org/mtik00/yamicache
        :alt: Travis Status

.. image:: https://readthedocs.org/projects/yamicache/badge/?version=latest
        :target: https://yamicache.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://coveralls.io/repos/github/mtik00/yamicache/badge.svg?branch=master
        :target: https://coveralls.io/github/mtik00/yamicache?branch=master
        :alt: Coveralls Status


Yet another in-memory caching package


* Free software: MIT license
* Documentation: https://yamicache.readthedocs.io.


Features
--------

* Memoization
* Selective caching based on decorators
* Mutli-threaded support
* Optional garbage collection thread
* Optional time-based cache expiration


Quick Start
-----------

.. code-block:: python

    from __future__ import print_function
    import time
    from yamicache import Cache
    c = Cache()
    class MyApp(object):
        @c.cached()
        def long_op(self):
                time.sleep(30)
                return 1

    app = MyApp()
    t_start = time.time()
    assert app.long_op() == 1  # takes 30s
    assert app.long_op() == 1  # takes 0s
    assert app.long_op() == 1  # takes 0s
    assert 1 < (time.time() - t_start) < 31


=======
History
=======

0.4.0 (2017-10-09)
------------------

* Added ``serialize()`` and ``deserialize()``


0.3.0 (2017-09-05)
------------------

* Added ``@clear_cache()`` decorator
* Added imports to allow for ``from yamicache import Cache``


0.2.0 (2017-09-03)
------------------

* Added cache key collision checking


0.1.1 (2017-09-01)
------------------

* Fix #1: ``Cache.cached()`` ignores ``timeout`` parameter


0.1.0 (2017-08-28)
------------------

* First release on PyPI.


