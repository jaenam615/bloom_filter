"""
Example usage of the Bloom filter implementation.
"""

from bloom_filter import BloomFilter


def basic_example():
    """Demonstrate basic usage of Bloom filter."""
    print("=" * 60)
    print("Basic Bloom Filter Example")
    print("=" * 60)
    
    # Create a Bloom filter for 1000 elements with 1% false positive rate
    bf = BloomFilter(expected_elements=1000, false_positive_rate=0.01)
    
    print(f"\nCreated Bloom filter:")
    print(f"  - Size: {bf.size} bits")
    print(f"  - Hash functions: {bf.hash_count}")
    
    # Add some fruits
    fruits = ["apple", "banana", "cherry", "date", "elderberry", "fig", "grape"]
    print(f"\nAdding fruits: {fruits}")
    for fruit in fruits:
        bf.add(fruit)
    
    # Check membership
    print("\nChecking membership:")
    for fruit in ["apple", "banana", "orange", "grape", "mango"]:
        result = "YES" if bf.contains(fruit) else "NO"
        print(f"  - Is '{fruit}' in the filter? {result}")
    
    # Display statistics
    print("\nFilter statistics:")
    stats = bf.get_stats()
    for key, value in stats.items():
        if isinstance(value, float):
            print(f"  - {key}: {value:.4f}")
        else:
            print(f"  - {key}: {value}")


def false_positive_demo():
    """Demonstrate false positive behavior."""
    print("\n" + "=" * 60)
    print("False Positive Rate Demonstration")
    print("=" * 60)
    
    # Create a small filter to increase false positive chances
    bf = BloomFilter(expected_elements=100, false_positive_rate=0.1)
    
    # Add numbers 0-99
    print("\nAdding numbers 0 to 99 to the filter...")
    for i in range(100):
        bf.add(i)
    
    # Test with numbers 100-199 (not in the filter)
    print("Testing with numbers 100-199 (not in the filter)...")
    false_positives = 0
    test_range = range(100, 200)
    
    for i in test_range:
        if bf.contains(i):
            false_positives += 1
    
    fpr = false_positives / len(test_range)
    print(f"\nResults:")
    print(f"  - Tests performed: {len(test_range)}")
    print(f"  - False positives: {false_positives}")
    print(f"  - Observed false positive rate: {fpr:.2%}")
    print(f"  - Expected false positive rate: ~10%")


def practical_example():
    """Demonstrate a practical use case."""
    print("\n" + "=" * 60)
    print("Practical Example: Username Availability Check")
    print("=" * 60)
    
    # Simulate a system with existing usernames
    existing_users = [
        "alice", "bob", "charlie", "david", "emma",
        "frank", "grace", "henry", "isabel", "jack"
    ]
    
    # Create Bloom filter for quick pre-check
    bf = BloomFilter(expected_elements=10000, false_positive_rate=0.001)
    
    print("\nRegistering existing users...")
    for user in existing_users:
        bf.add(user)
    
    print(f"Registered {len(existing_users)} users")
    
    # Check if usernames are available
    test_usernames = ["alice", "zoe", "bob", "mike", "charlie", "nina"]
    
    print("\nChecking username availability:")
    for username in test_usernames:
        if bf.contains(username):
            print(f"  - '{username}': Might be taken (need database check)")
        else:
            print(f"  - '{username}': Definitely available!")


def size_comparison():
    """Compare Bloom filter size with storing actual elements."""
    print("\n" + "=" * 60)
    print("Space Efficiency Comparison")
    print("=" * 60)
    
    num_elements = 100000
    
    # Calculate Bloom filter size
    bf = BloomFilter(expected_elements=num_elements, false_positive_rate=0.01)
    bloom_bits = bf.size
    bloom_bytes = bloom_bits / 8
    bloom_kb = bloom_bytes / 1024
    
    # Estimate size of storing actual strings (assuming average 10 chars)
    avg_string_size = 10  # bytes
    set_bytes = num_elements * avg_string_size
    set_kb = set_bytes / 1024
    
    print(f"\nStoring {num_elements:,} elements:")
    print(f"\nBloom Filter:")
    print(f"  - Bits: {bloom_bits:,}")
    print(f"  - Size: {bloom_kb:.2f} KB")
    
    print(f"\nActual Set (estimated):")
    print(f"  - Size: {set_kb:.2f} KB")
    
    print(f"\nSpace savings: {(1 - bloom_kb/set_kb)*100:.1f}%")
    print(f"Trade-off: {bf.get_stats()['estimated_false_positive_rate']:.2%} false positive rate")


def main():
    """Run all examples."""
    basic_example()
    false_positive_demo()
    practical_example()
    size_comparison()
    
    print("\n" + "=" * 60)
    print("Examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
