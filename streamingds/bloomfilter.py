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

from bitstring import BitArray

from streamingds.hashing import Hashing


class BloomFilter(Hashing):
    """A bloom filter implementation for a space efficient way to test for
    membership in a large amount of data.
    """

    def __init__(self, capacity, error_rate=0.001):
        """Initialize the filter.

        `capacity` and `error_rate` define the probabilities for false
        positives. Given these two parameters, the filter is able to store at
        least `capacity` amount of items with the given `error_rate` for false
        positives.

        :param capacity: minimum number of documents with `error_rate` false
                         positives
        :type capacity: int
        :param error_rate: error rate for false positives
        :type error_rate: float
        """
        if not (0 < error_rate < 1):
            raise ValueError('error_rate must be 0 and 1.')
        if capacity <= 0:
            raise ValueError('capacity must be greater than 1')

        self._capacity = capacity
        self._error_rate = error_rate

        bits = int(math.ceil(
            (capacity * math.log(1/error_rate) / math.log(2) ** 2)))
        num_hash_fns = int(round(bits * math.log(2) / capacity))

        super(BloomFilter, self).__init__(num_hash_fns, bits)

    @property
    def bitarray(self):
        if not hasattr(self, '_bitarray'):
            self._bitarray = BitArray(self.bits)
        return self._bitarray

    def __contains__(self, key):
        """Check membership of a key in this filter."""
        return self.bitarray.all(1, self.hash_values(key))

    def add(self, key):
        """Add a key to this filter."""
        self.bitarray.set(1, self.hash_values(key))

    def __len__(self):
        """Get the number of elements in the filter."""
        m = self.bitarray.count(1)
        a = (self.bits * math.log(1 - (float(m) / self.bits)))
        return - a / self.num_hash_fns
