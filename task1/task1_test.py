import unittest

from task1 import BloomFilter, check_password_uniqueness


class TestBloomFilterPasswordUniqueness(unittest.TestCase):
    def setUp(self):
        self.bloom = BloomFilter(size=1000, num_hashes=3)

    def test_check_password_uniqueness(self):
        test_cases = [
            {
                "existing_passwords": ["password123", "admin123", "qwerty123"],
                "new_passwords": ["password123", "newpassword", "admin123", "guest", None, 12345],
                "expected": {
                    "password123": "already used",
                    "newpassword": "unique",
                    "admin123": "already used",
                    "guest": "unique",
                    None: "invalid",
                    12345: "invalid"
                },
            }
        ]

        for case in test_cases:
            for password in case["existing_passwords"]:
                self.bloom.add(password)

            results = check_password_uniqueness(self.bloom, case["new_passwords"])
            self.assertEqual(results, case["expected"])

    def test_invalid_item_addition(self):
        with self.assertRaises(ValueError):
            self.bloom.add(None)

    def test_invalid_item_contains(self):
        with self.assertRaises(ValueError):
            self.bloom.contains(None)


if __name__ == "__main__":
    unittest.main()