import pytest

from bloom_filter import BloomFilter

@pytest.fixture
def bloom_filter():
    return BloomFilter(
        size = 16,
        k = 3
    )

def test_add(bloom_filter):
    bloom_filter.add("jaehee")

    assert sum(bloom_filter.bitmap) == 3

    bloom_filter.add("apple")
    assert sum(bloom_filter.bitmap) == 6

def test_contains(bloom_filter):
    bloom_filter.add("jaehee")

    assert bloom_filter.contains("jaehee") == True

def test_does_not_contain(bloom_filter):
    bloom_filter.add("jaehee")

    assert bloom_filter.contains("apple") == False
