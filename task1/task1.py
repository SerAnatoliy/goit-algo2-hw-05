import mmh3


class BloomFilter:
    def __init__(self, size, num_hashes):
        self.size = size
        self.num_hashes = num_hashes
        self.bit_array = [0] * size

    def add(self, item):
        if item is None:
            raise ValueError("Item cannot be None")
        item_str = str(item)
        for i in range(self.num_hashes):
            index = mmh3.hash(item_str, i) % self.size
            self.bit_array[index] = 1

    def contains(self, item):
        if item is None:
            raise ValueError("Item cannot be None")
        item_str = str(item)
        for i in range(self.num_hashes):
            index = mmh3.hash(item_str, i) % self.size
            if self.bit_array[index] == 0:
                return False
        return True


def check_password_uniqueness(bloom_filter, passwords):
    results = {}
    for password in passwords:
        if password is None or not isinstance(password, str):
            results[password] = "invalid"
        elif bloom_filter.contains(password):
            results[password] = "already used"
        else:
            results[password] = "unique"
            bloom_filter.add(password)
    return results