# vim: set fileencoding=utf-8 :
from __future__ import (absolute_import, division, print_function,
                        with_statement)

import random

from cytoolz import juxt
from pyhashxx import hashxx


class Hashing(object):
    """Simple class to help developing hash based datastructures like the
    count-min sketch or bloomfilters.
    """

    def __init__(self, num_hash_fns, bits):
        """Initialize the array of `hashfunctions`."""
        self.bits = bits
        self.num_hash_fns = num_hash_fns

    @property
    def bits(self):
        return self._bits

    @bits.setter
    def bits(self, value):
        self._bits = value

    @property
    def num_hash_fns(self):
        return self._num_hash_fns

    @num_hash_fns.setter
    def num_hash_fns(self, value):
        self._num_hash_fns = value

    @property
    def seeds(self):
        if not hasattr(self, '_seeds'):
            self._seeds = [random.randint(0, 2 ** 32)
                           for _ in range(self.num_hash_fns)]
        return self._seeds

    def _gen_hash_fn(self, seed, num_hash_fns):
        return lambda x: hashxx(str(x), seed=seed) % self.bits

    @property
    def hash_functions(self):
        if not hasattr(self, '_hash_functions'):
            self._hash_functions = [
                self._gen_hash_fn(s, self.num_hash_fns)
                for s in self.seeds]
        return self._hash_functions

    def hash_values(self, key):
        """Return the hashes for the given key."""
        return juxt(self.hash_functions)(key)
