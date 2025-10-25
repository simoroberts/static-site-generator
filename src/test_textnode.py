import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_eq_false(self):
        node = TextNode("This is a plain text node", TextType.PLAIN)
        node2 = TextNode("This is a plain text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_eq_false2(self):
        node = TextNode("This is a plain text node", TextType.PLAIN)
        node2 = TextNode("This is an italicized text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_eq_false_url(self):
        node = TextNode("This is a link", TextType.LINK, url="http://127.0.0.1")
        node2 = TextNode("This is a link", TextType.LINK, url=None)
        self.assertNotEqual(node, node2)
    
    def test_repr(self):
        node = TextNode("This is a link", TextType.LINK, url="http://127.0.0.1")
        self.assertEqual(
                "TextNode(This is a link, link, http://127.0.0.1)", repr(node)
        )
if __name__ == "__main__":
    unittest.main()
