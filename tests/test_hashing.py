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

from random import randint, sample

import pytest

from streamingds.hashing import Hashing


_WORDS = """Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam
nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam
voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita
kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem
ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod
tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At
vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd
gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.""".split(
    ' ')


@pytest.mark.parametrize(("slices,bits_ps, key_counter"),
                         [(randint(100, 100),
                           randint(100, 1000),
                           randint(1, 100)
                           ) for _ in range(100)]
                         )
def test_simple_hashing(slices, bits_ps, key_counter):
    h = Hashing(slices, bits_ps)

    keys = ['-'.join(sample(_WORDS, 4))
            for _ in range(key_counter)]

    assert len(keys) == key_counter

    for key in keys:
        assert list(h.hash_values(key)) == list(h.hash_values(key))
