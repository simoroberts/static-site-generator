import unittest

from htmlnode import HTMLNode 

class TestHtmlNode(unittest.TestCase):
    def test_values(self):
        node = HTMLNode("p", "Hello World")
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "Hello World")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_props_to_html_eq(self):
        node = HTMLNode(
                "a", 
                "Hello World", 
                None, 
                {"href": "https://www.google.com", "target": "_blank"}
        )
        self.assertEqual(
                node.props_to_html(), 
                " href=\"https://www.google.com\" target=\"_blank\""
        )

    def test_repr(self):
        node = HTMLNode(
                "a", 
                "Hello World", 
                [
                    HTMLNode("p", "Goodbye"), HTMLNode("p", "World")
                ], 
                {
                    "href": "https://127.0.0.1"
                }
        )
        self.assertEqual(
                "HTMLNode(a, Hello World, [HTMLNode(p, Goodbye, None, None), HTMLNode(p, World, None, None)], {'href': 'https://127.0.0.1'})",
                repr(node)
        )

if __name__ == "__main__":
    unittest.main()
