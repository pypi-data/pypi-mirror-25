|PyPI version| |Build Status| |Supported Python Versions|

TTL Memoized - A memoized decorator with TTL (time-to-live) support.
====================================================================

The idea of ``memoized`` is great, as some resources are expensive, so
you want to cache them.

However, there isn't a memoized lib support TTL (time-to-live) at the
moment, or I haven't find any thing yet.

So I implement this
`ttl\_memoized <http://github.com/tly1980/ttl_memoized>`__ to fill in
the gap here.

Also, this lib is meant to be thread-safe, using
`threading.local <https://docs.python.org/2/library/threading.html#threading.local>`__
object to store the variables.

Installation:
-------------

Should be faily simple using pip:

::

    pip install ttl_memoized

Usage
-----

The usage is simple, and the best way to explain it, is with my test
cases:

::

    def test_basic():

      @memoized(ttl=0.5)
      def a(name):
        return datetime.datetime.now()

      @memoized(ttl=0.5)
      def b(name, *args, **kwargs):
        return datetime.datetime.now()

      a1 = a(1)
      b1 = b(1, 2, 3, what='ever', you='want', to='be')

      for i in range(100):
        assert a1 == a(1)

      for i in range(100):
        assert b1 is b(1, 2, 3, what='ever', you='want', to='be')

      a2 = a(2)
      assert a2 != a1

      # let the cache expired...
      time.sleep(0.51)

      assert a(1) != a1
      assert b1 != b(1, 2, 3, what='ever', you='want', to='be')

Ceveat
------

The parameter for the functions is required to be serializable with
`json <https://docs.python.org/2/library/json.html>`__ libs, as the lib
is using json to build the keys from parameters.

.. |PyPI version| image:: https://badge.fury.io/py/ttl_memoized.svg
   :target: https://badge.fury.io/py/ttl_memoized
.. |Build Status| image:: https://travis-ci.org/tly1980/ttl_memoized.svg?branch=master
   :target: https://travis-ci.org/tly1980/ttl_memoized
.. |Supported Python Versions| image:: https://img.shields.io/badge/python-2.6%2C%202.7%2C%203.3%2C%203.4%2C%203.5%2C%203.6-blue.svg
   :target: https://travis-ci.org/tly1980/ttl_memoized


