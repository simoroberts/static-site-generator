import unittest

from htmlnode import HTMLNode, ParentNode, LeafNode

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

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_empty_children(self):
        parent_node = ParentNode("div", [])
        self.assertEqual(parent_node.to_html(), "<div></div>")

    def test_to_html_no_children(self):
        parent_node = ParentNode("div", None)
        self.assertRaises(expected_exception=ValueError)

    def test_to_html_no_tag(self):
        parent_node = ParentNode(None, [])
        self.assertRaises(expected_exception=ValueError)

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click", props={"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), "<a href=\"https://www.google.com\">Click</a>")

    def test_leaf_to_html_b(self):
        node = LeafNode("b", "This is bold text.")
        self.assertEqual(node.to_html(), "<b>This is bold text.</b>")

if __name__ == "__main__":
    unittest.main()
