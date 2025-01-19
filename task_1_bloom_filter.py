import mmh3


class BloomFilter:
    def __init__(self, size, num_hashes):
        self.size = size
        self.num_hashes = num_hashes
        self.bit_array = [0] * size

    def add(self, item):
        for i in range(self.num_hashes):
            index = mmh3.hash(item, i) % self.size
            self.bit_array[index] = 1

    def contains(self, item):
        for i in range(self.num_hashes):
            index = mmh3.hash(item, i) % self.size
            if self.bit_array[index] == 0:
                return False
        return True


def check_password_uniqueness(bloom_filter, passwords):
    results = {}
    for password in passwords:
        if bloom_filter.contains(password):
            results[password] = "unique"
        else:
            results[password] = "already exists"
    return results


if __name__ == "__main__":
    # Bloom filter initialisation
    bloom = BloomFilter(size=1000, num_hashes=3)

    # Add passwords to the bloom filter
    passwords = ["password123", "admin123", "querty123"]
    for password in passwords:
        bloom.add(password)

    # Check if the passwords are unique
    new_passwords_to_check = ["password123", "newpassword", "admin123", "guest"]
    results = check_password_uniqueness(bloom, new_passwords_to_check)

    # Print the results
    for password, status in results.items():
        print(f"Password: {password} -  {status}")
