"""
Bloom Filter implementation in Python.

A Bloom filter is a space-efficient probabilistic data structure used to test
whether an element is a member of a set. False positives are possible, but
false negatives are not.
"""

import hashlib
import math
from typing import Any


class BloomFilter:
    """
    A Bloom filter implementation using multiple hash functions.
    
    Attributes:
        size: The size of the bit array
        hash_count: The number of hash functions to use
        bit_array: The bit array for storing hashed values
    """
    
    def __init__(self, expected_elements: int = 1000, false_positive_rate: float = 0.01):
        """
        Initialize a Bloom filter.
        
        Args:
            expected_elements: Expected number of elements to be added
            false_positive_rate: Desired false positive probability (between 0 and 1)
        
        Raises:
            ValueError: If parameters are out of valid range
        """
        if expected_elements <= 0:
            raise ValueError("Expected elements must be positive")
        if not 0 < false_positive_rate < 1:
            raise ValueError("False positive rate must be between 0 and 1")
        
        # Calculate optimal size and number of hash functions
        self.size = self._calculate_size(expected_elements, false_positive_rate)
        self.hash_count = self._calculate_hash_count(self.size, expected_elements)
        self.bit_array = [False] * self.size
        self.element_count = 0
    
    @staticmethod
    def _calculate_size(n: int, p: float) -> int:
        """
        Calculate optimal bit array size.
        
        Formula: m = -(n * ln(p)) / (ln(2)^2)
        
        Args:
            n: Expected number of elements
            p: Desired false positive rate
            
        Returns:
            Optimal size of bit array
        """
        m = -(n * math.log(p)) / (math.log(2) ** 2)
        return int(m)
    
    @staticmethod
    def _calculate_hash_count(m: int, n: int) -> int:
        """
        Calculate optimal number of hash functions.
        
        Formula: k = (m / n) * ln(2)
        
        Args:
            m: Size of bit array
            n: Expected number of elements
            
        Returns:
            Optimal number of hash functions
        """
        k = (m / n) * math.log(2)
        return max(1, int(k))
    
    def _hash(self, item: Any, seed: int) -> int:
        """
        Generate a hash value for an item with a given seed.
        
        Args:
            item: The item to hash
            seed: Seed value for the hash function
            
        Returns:
            Hash value modulo the bit array size
        """
        # Convert item to bytes using repr to avoid hash collisions
        # between different types with same string representation
        item_bytes = repr(item).encode('utf-8')
        # Use hashlib with seed for different hash functions
        hash_obj = hashlib.sha256(item_bytes + str(seed).encode('utf-8'))
        # Return hash value modulo size
        return int(hash_obj.hexdigest(), 16) % self.size
    
    def add(self, item: Any) -> None:
        """
        Add an item to the Bloom filter.
        
        Args:
            item: The item to add to the filter
        """
        for i in range(self.hash_count):
            index = self._hash(item, i)
            self.bit_array[index] = True
        self.element_count += 1
    
    def contains(self, item: Any) -> bool:
        """
        Check if an item might be in the Bloom filter.
        
        Args:
            item: The item to check
            
        Returns:
            True if the item might be in the set (could be false positive),
            False if the item is definitely not in the set
        """
        for i in range(self.hash_count):
            index = self._hash(item, i)
            if not self.bit_array[index]:
                return False
        return True
    
    def __contains__(self, item: Any) -> bool:
        """Support 'in' operator for membership testing."""
        return self.contains(item)
    
    def get_stats(self) -> dict:
        """
        Get statistics about the Bloom filter.
        
        Returns:
            Dictionary containing filter statistics
        """
        bits_set = sum(self.bit_array)
        load_factor = bits_set / self.size if self.size > 0 else 0
        
        # Estimated false positive rate based on current load
        # Formula: (1 - e^(-k*n/m))^k
        if self.size > 0 and self.element_count > 0:
            estimated_fpr = (1 - math.exp(-self.hash_count * self.element_count / self.size)) ** self.hash_count
        else:
            estimated_fpr = 0
        
        return {
            'size': self.size,
            'hash_count': self.hash_count,
            'element_count': self.element_count,
            'bits_set': bits_set,
            'load_factor': load_factor,
            'estimated_false_positive_rate': estimated_fpr
        }
    
    def clear(self) -> None:
        """Clear all elements from the Bloom filter."""
        self.bit_array = [False] * self.size
        self.element_count = 0
