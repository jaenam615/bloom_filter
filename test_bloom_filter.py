"""
Unit tests for the Bloom filter implementation.
"""

import unittest
from bloom_filter import BloomFilter


class TestBloomFilter(unittest.TestCase):
    """Test cases for the BloomFilter class."""
    
    def test_initialization(self):
        """Test that Bloom filter initializes correctly."""
        bf = BloomFilter(expected_elements=100, false_positive_rate=0.01)
        self.assertIsNotNone(bf.bit_array)
        self.assertGreater(bf.size, 0)
        self.assertGreater(bf.hash_count, 0)
        self.assertEqual(bf.element_count, 0)
    
    def test_invalid_initialization(self):
        """Test that invalid parameters raise errors."""
        with self.assertRaises(ValueError):
            BloomFilter(expected_elements=0, false_positive_rate=0.01)
        
        with self.assertRaises(ValueError):
            BloomFilter(expected_elements=100, false_positive_rate=0)
        
        with self.assertRaises(ValueError):
            BloomFilter(expected_elements=100, false_positive_rate=1.5)
    
    def test_add_and_contains(self):
        """Test adding elements and checking membership."""
        bf = BloomFilter(expected_elements=100, false_positive_rate=0.01)
        
        # Add some elements
        bf.add("apple")
        bf.add("banana")
        bf.add("cherry")
        
        # Check they are in the filter
        self.assertTrue(bf.contains("apple"))
        self.assertTrue(bf.contains("banana"))
        self.assertTrue(bf.contains("cherry"))
        
        # Check element count
        self.assertEqual(bf.element_count, 3)
    
    def test_contains_operator(self):
        """Test that 'in' operator works."""
        bf = BloomFilter(expected_elements=100, false_positive_rate=0.01)
        
        bf.add("test")
        self.assertTrue("test" in bf)
        self.assertFalse("not_added" in bf)
    
    def test_negative_membership(self):
        """Test that elements not added are not found (no false negatives)."""
        bf = BloomFilter(expected_elements=100, false_positive_rate=0.01)
        
        bf.add("element1")
        bf.add("element2")
        
        # These should definitely not be in the filter
        self.assertFalse(bf.contains("not_added"))
        self.assertFalse(bf.contains("also_not_added"))
    
    def test_different_types(self):
        """Test that different data types can be added."""
        bf = BloomFilter(expected_elements=100, false_positive_rate=0.01)
        
        bf.add(123)
        bf.add(45.67)
        bf.add("string")
        bf.add(True)
        
        self.assertTrue(bf.contains(123))
        self.assertTrue(bf.contains(45.67))
        self.assertTrue(bf.contains("string"))
        self.assertTrue(bf.contains(True))
    
    def test_false_positive_rate(self):
        """Test that false positive rate is approximately as expected."""
        # Use a larger filter for more reliable statistics
        expected_elements = 1000
        target_fpr = 0.01
        bf = BloomFilter(expected_elements=expected_elements, false_positive_rate=target_fpr)
        
        # Add expected number of elements
        for i in range(expected_elements):
            bf.add(f"element_{i}")
        
        # Test with elements not in the filter
        false_positives = 0
        test_count = 1000
        for i in range(test_count):
            if bf.contains(f"not_in_filter_{i}"):
                false_positives += 1
        
        observed_fpr = false_positives / test_count
        
        # Allow some tolerance (false positive rate should be roughly within 5x of target)
        self.assertLess(observed_fpr, target_fpr * 5,
                       f"False positive rate {observed_fpr} is too high (target: {target_fpr})")
    
    def test_clear(self):
        """Test that clear() resets the filter."""
        bf = BloomFilter(expected_elements=100, false_positive_rate=0.01)
        
        bf.add("element1")
        bf.add("element2")
        self.assertTrue(bf.contains("element1"))
        self.assertEqual(bf.element_count, 2)
        
        bf.clear()
        
        self.assertEqual(bf.element_count, 0)
        self.assertEqual(sum(bf.bit_array), 0)
        # After clearing, elements should not be found
        self.assertFalse(bf.contains("element1"))
    
    def test_get_stats(self):
        """Test that statistics are returned correctly."""
        bf = BloomFilter(expected_elements=100, false_positive_rate=0.01)
        
        stats = bf.get_stats()
        self.assertIn('size', stats)
        self.assertIn('hash_count', stats)
        self.assertIn('element_count', stats)
        self.assertIn('bits_set', stats)
        self.assertIn('load_factor', stats)
        self.assertIn('estimated_false_positive_rate', stats)
        
        # Initially, no elements added
        self.assertEqual(stats['element_count'], 0)
        self.assertEqual(stats['bits_set'], 0)
        self.assertEqual(stats['load_factor'], 0)
        
        # Add some elements
        bf.add("test1")
        bf.add("test2")
        
        stats = bf.get_stats()
        self.assertEqual(stats['element_count'], 2)
        self.assertGreater(stats['bits_set'], 0)
        self.assertGreater(stats['load_factor'], 0)
    
    def test_large_dataset(self):
        """Test with a larger dataset."""
        bf = BloomFilter(expected_elements=10000, false_positive_rate=0.001)
        
        # Add 10000 elements
        for i in range(10000):
            bf.add(f"item_{i}")
        
        # All added items should be found
        for i in range(10000):
            self.assertTrue(bf.contains(f"item_{i}"),
                          f"Element 'item_{i}' should be in the filter")
        
        # Check that element count is correct
        self.assertEqual(bf.element_count, 10000)
    
    def test_duplicate_adds(self):
        """Test adding duplicate elements."""
        bf = BloomFilter(expected_elements=100, false_positive_rate=0.01)
        
        bf.add("duplicate")
        bf.add("duplicate")
        bf.add("duplicate")
        
        # Should still be found
        self.assertTrue(bf.contains("duplicate"))
        
        # Note: element_count will be 3 because we don't track uniqueness
        # This is expected behavior for a Bloom filter
        self.assertEqual(bf.element_count, 3)
    
    def test_empty_filter(self):
        """Test operations on an empty filter."""
        bf = BloomFilter(expected_elements=100, false_positive_rate=0.01)
        
        # Should not contain anything
        self.assertFalse(bf.contains("anything"))
        self.assertFalse(bf.contains(123))
        
        stats = bf.get_stats()
        self.assertEqual(stats['element_count'], 0)
        self.assertEqual(stats['bits_set'], 0)


if __name__ == '__main__':
    unittest.main()
