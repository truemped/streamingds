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

from random import randint

import pytest

from streamingds.bloomfilter import BloomFilter


def test_simple_bloomfilter():
    bf = BloomFilter(100)
    bf.add('test')
    assert 'test' in bf

    bf.add('anothertest')
    assert 'anothertest' in bf

    assert 'notthere' not in bf


@pytest.mark.parametrize("capacity",
                         [(randint(1000, 10000)) for _ in range(10)]
                         )
def test_bloom_filter(capacity):
    replays = randint(0, capacity)

    bf = BloomFilter(capacity)

    keys = []
    for i in range(replays):
        key = 'bloom-filter-key-%s' % i
        keys.append(key)
        bf.add(key)

    for key in keys:
        assert key in bf
        assert 'not-%s' % key not in bf
