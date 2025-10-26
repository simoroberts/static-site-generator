import unittest

from textnode import TextNode, TextType, text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_eq_false(self):
        node = TextNode("This is a plain text node", TextType.TEXT)
        node2 = TextNode("This is a plain text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_eq_false2(self):
        node = TextNode("This is a plain text node", TextType.TEXT)
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

class TestTextNodeToHTML(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_image(self):
        node = TextNode("This is an image", TextType.IMAGE, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://www.boot.dev", "alt": "This is an image"},
        )

    def test_italic(self):
        node = TextNode("This is italics", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is italics")

if __name__ == "__main__":
    unittest.main()
