import unittest

from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter

class TestSplitDelimiter(unittest.TestCase):
    def test_bold(self):
        node = TextNode("This is text with **bolded phrase** in the middle", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
                new_nodes, 
                [
                    TextNode("This is text with ", TextType.TEXT),
                    TextNode("bolded phrase", TextType.BOLD),
                    TextNode(" in the middle", TextType.TEXT)
                ]
        )

    def test_multiple_bold(self):
        node = TextNode("This is text with **bolded phrase** in the middle and **end**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
                new_nodes, 
                [
                    TextNode("This is text with ", TextType.TEXT),
                    TextNode("bolded phrase", TextType.BOLD),
                    TextNode(" in the middle and ", TextType.TEXT),
                    TextNode("end", TextType.BOLD),
                ]
        )

    def test_code(self):
        node = TextNode("This is text with `code` in the middle", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
                new_nodes, 
                [
                    TextNode("This is text with ", TextType.TEXT),
                    TextNode("code", TextType.CODE),
                    TextNode(" in the middle", TextType.TEXT),
                ]
        )

    def test_italic(self):
        node = TextNode("This is text with _italics_ in the middle", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(
                new_nodes, 
                [
                    TextNode("This is text with ", TextType.TEXT),
                    TextNode("italics", TextType.ITALIC),
                    TextNode(" in the middle", TextType.TEXT),
                ]
        )

    def test_bold_code(self):
        node = TextNode("This is text with **bolded phrase** in the middle and `some code`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
        self.assertEqual(
                new_nodes, 
                [
                    TextNode("This is text with ", TextType.TEXT),
                    TextNode("bolded phrase", TextType.BOLD),
                    TextNode(" in the middle and ", TextType.TEXT),
                    TextNode("some code", TextType.CODE),
                ]
        )
