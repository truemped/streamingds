Development environment
=======================

The most simple way is to use a virtual environment:

    $ mkvirtualenv streamingds
    $ pip install -r requirements.txt
    $ pip install -r requirements-test.txt
    $ python setup.py develop

If you want to test or work on cython, you need to install cython as well:

    $ pip install cython


Testing
-------

To run the tests simply execute:

    $ py.test -m 'not slowtest'

This will execute the unittests except for those having the `slowtest` mark.


Creating a pull request
-----------------------

A pull request can also be a place for discussion and code review, so do not
hesitate to create it early on.
