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

from hashlib import sha224
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


@pytest.mark.parametrize("capacity, max_keys",
                         [(randint(10000, 100000),
                           randint(1, 50)) for _ in range(100)]
                         )
def test_bloom_filter(capacity, max_keys):
    replays = randint(0, max_keys)

    bf = BloomFilter(capacity)

    keys = []
    errors = []
    for i in range(replays):
        key = 'bloom-filter-key-%s' % i
        keys.append(key)
        bf.add(key)

    for key in keys:
        assert key in bf
        if 'this-should-not-%s' % key in bf:
            errors.append(1)

    actual = len(errors) / float(capacity)
    assert actual <= 0.01


def gethash(key):
    return sha224(str(key)).hexdigest()


def generate_url(n):
    return 'http://www.news.de/section/subsection/%d/%s.html' % (n, gethash(n))


@pytest.mark.parametrize("n, r",
                         [(n, r)
                          for n in [1000, 10000, 100000, 1000000]
                          for r in [0.1, 0.01, 0.001, 0.0001, 0.00001]])
def test_bloomfilter_urls(n, r):
    bf = BloomFilter(n, error_rate=r)
    misses = []
    for key in xrange(n):
        url = generate_url(key)
        if url in bf:
            # false positive!
            misses.append(key)
        else:
            bf.add(url)

    observed_count = len(misses)
    observed_rate = observed_count / float(n)

    assert observed_rate <= r
