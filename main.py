from bloom_filter import BloomFilter

if __name__ == "__main__":
    bf = BloomFilter(
        size = 16
    )

    print(bf.bitmap)