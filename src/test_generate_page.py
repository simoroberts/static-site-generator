import unittest

from generate_page import extract_title

class TestGeneratePage(unittest.TestCase):
    def test_extract_title(self):
        title = extract_title("# Hello")
        self.assertEqual("Hello", title)
        

