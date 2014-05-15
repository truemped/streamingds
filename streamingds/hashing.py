# vim: set fileencoding=utf-8 :
#
# Copyright (c) 2013 Daniel Truemper <truemped at googlemail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
from __future__ import (absolute_import, division, print_function,
                        with_statement)

import math
import random
import sys


_int_size = len(bin(sys.maxint)) - 1
_int_mask = (1 << _int_size) - 1
_random_odd_int = lambda: (int(random.getrandbits(_int_size - 2))) << 1 | 1
_log2 = lambda x: math.log(x) / math.log(2.0)
_multiply_shift = lambda m, a, x: ((a * x) & _int_mask) >> (_int_size - m)


class Hashing(object):
    """Simple class to help developing hash based datastructures like the
    count-min sketch or bloomfilters.
    """

    def __init__(self, num_slices, num_bits_per_slice):
        """Initialize the array of `hashfunctions`."""
        self._num_bits_per_slice = num_bits_per_slice
        self._num_slices = num_slices

    @property
    def bits_per_slice(self):
        return self._num_bits_per_slice

    @property
    def slices(self):
        return self._num_slices

    @property
    def hash_functions(self):
        if not hasattr(self, '_hash_functions'):
            self._hash_functions = [_random_odd_int()
                                    for i in range(self.slices)]
        return self._hash_functions

    def hash_values(self, key):
        """Return the hashes for the given key."""
        ix = abs(hash(key))
        hashes = []
        for i in range(self.slices):
            hf = self.hash_functions[i]
            hashes.append(_multiply_shift(self.slices, hf, ix))

        return hashes
