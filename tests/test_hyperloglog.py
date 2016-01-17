# vim: set fileencoding=utf-8 :
from streamingds.hyperloglog import get_alpha
from streamingds.hyperloglog import HyperLogLog

import pytest
from random import sample

def test_simple_hyperloglog():
    hll = HyperLogLog(12)

    num_elements = 500000

    elements = sample(xrange(5000000), num_elements)
    hll.add(*elements)

    cardinality = hll.cardinality()

    margin = cardinality * hll.error_rate
    assert num_elements - margin <= cardinality <= num_elements + margin

def test_invalid_p_value():
    with pytest.raises(ValueError):
        hll = HyperLogLog(0)

def test_get_alpha():
    assert get_alpha(4) == 0.673
    assert get_alpha(5) == 0.697
    assert get_alpha(6) == 0.709
    assert round(get_alpha(7), 3) == 0.715

def test_merge_hlls_with_same_precisions():
    hll1 = HyperLogLog(5)
    hll1.add(xrange(500))

    hll2 = HyperLogLog(5)

    hll2.merge(hll1)
    assert hll2._registers == hll1._registers

def test_merge_hlls_with_different_precisions():
    with pytest.raises(ValueError):
        hll1 = HyperLogLog(6)
        hll2 = HyperLogLog(7)

        hll1.merge(hll2)
