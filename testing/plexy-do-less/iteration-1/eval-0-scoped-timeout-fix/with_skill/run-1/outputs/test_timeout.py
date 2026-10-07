import unittest

from timeout import milliseconds_to_seconds, request_options


class TimeoutTest(unittest.TestCase):
    def test_conversion(self):
        for milliseconds, seconds in [(0, 0), (1, 0.001), (1500, 1.5), (60000, 60)]:
            with self.subTest(milliseconds=milliseconds):
                self.assertEqual(milliseconds_to_seconds(milliseconds), seconds)

    def test_negative_timeout(self):
        with self.assertRaisesRegex(ValueError, "timeout must be non-negative"):
            milliseconds_to_seconds(-1)

    def test_request_options(self):
        self.assertEqual(request_options(1500), {"timeout": 1.5, "retries": 2})
        with self.assertRaises(ValueError):
            request_options(-1)


if __name__ == "__main__":
    unittest.main()