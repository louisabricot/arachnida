""" Tests for parsing of the binary's argument """

import unittest


class TestParse(unittest.TestCase):
    """Tests the parsing of the program arguments"""

    def test_sum(self):
        """To check that github action works"""
        self.assertEqual(sum([1, 2]), 3, "Should be 3")


if __name__ == "__main__":
    unittest.main()
