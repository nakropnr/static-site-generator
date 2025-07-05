import unittest

from extract_title import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        text = "# heading"
        self.assertEqual(extract_title(text), "heading")


if __name__ == "__main__":
    unittest.main()