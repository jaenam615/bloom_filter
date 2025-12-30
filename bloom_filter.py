import hashlib
from bitarray import bitarray


class BloomFilter:
    def __init__(self, size: int, k: int):
        self.size = size
        self.k = k
        self.bitmap = bitarray(size)
        self.bitmap.setall(0)

    def _hash(self, item: str, seed: int) -> int:
        h = hashlib.sha256(f"{item}:{seed}".encode()).hexdigest()
        return int(h, 16) % self.size

    def add(self, item: str):
        for i in range(self.k):
            idx = self._hash(item, i)
            self.bitmap[idx] = 1

    def contains(self, item: str) -> bool:
        for i in range(self.k):
            idx = self._hash(item, i)
            if self.bitmap[idx] == 0:
                return False
        return True