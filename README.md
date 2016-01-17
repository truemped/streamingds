Streaming Data Structures
=========================

This library contains a set of sketching or hash-based algorithms.

|TravisImage|_ |RequiresIo|_

.. |TravisImage| image:: https://travis-ci.org/truemped/streamingds.png?branch=master
.. _TravisImage: https://travis-ci.org/truemped/streamingds

.. |RequiresIo| image:: https://requires.io/github/truemped/streamingds/requirements.svg?branch=master
.. _RequiresIo: https://requires.io/github/truemped/streamingds/requirements/?branch=master


Bloom Filter
------------

A [bloom filter](http://en.wikipedia.org/wiki/Bloom_filter) checks whether an
element has already been seen given a configurable false positive rate.

    >>> from streamingds.bloomfilter import BloomFilter
    >>> capacity = 1000
    >>> error_rate = 0.01
    >>> bf = BloomFilter(capacity, error_rate)
    >>> bf.add('test')
    >>> 'test' in bf
    True
    >>> 'that' in bf
    False


Count-min sketch
----------------

A [count-min sketch](http://en.wikipedia.org/wiki/Count-Min_sketch) estimates
the number of times an element has been seen. This implementation also keeps
track of the top k elements.

    >>> from streamingds.countminsketch import CountMinSketch
    >>> delta = 10 ** -7
    >>> epsilon = 0.005
    >>> topK = 50
    >>> cms = CountMinSketch(delta, epsilon, topK)
    >>> cms.update('www.google.com')
    >>> cms.get('www.google.com')
    1
    >>> cms.update('www.google.com', 12)
    >>> cms.get('www.google.com')
    13
    >>> cms.update('www.yahoo.com', 20)
    >>> cms.get_ranking()
    {0: (20, 'www.yahoo.com')
     1: (13, 'www.google.com')}


HyperLogLog
-----------

A [HyperLogLog](http://research.google.com/pubs/pub40671.html) estimates the
number of distinct items.

    >>> from random import sample
    >>> from streamingds.hyperloglog import HyperLogLog
    >>> hll = HyperLogLog(12)
    >>> num_elements = 500000
    >>> elements = sample(xrange(5000000), num_elements)
    >>> hll.add(*elements)
    >>> hll.cardinality()
    495079.71125622035


License
-------

MIT. See LICENSE
