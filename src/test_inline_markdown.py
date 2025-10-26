import unittest

from textnode import TextNode, TextType
from inline_markdown import (
        split_nodes_delimiter,
        split_nodes_image,
        split_nodes_link,
        extract_markdown_images, 
        extract_markdown_links,
        text_to_textnodes
)

class TestInlineMarkdown(unittest.TestCase):
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

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://www.google.com) plus [this link](http://localhost:8080)"
        )
        self.assertListEqual([("link", "https://www.google.com"), ("this link", "http://localhost:8080")], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes,
        )



    def test_split_images_no_image(self):
        node = TextNode(
            "This is text with an ",
            TextType.TEXT,
        )
        node2 = TextNode(
            "This is another",
            TextType.TEXT,
        )

        new_nodes = split_nodes_image([node, node2])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("This is another", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "Text with a [nowhere](http://localhost:8080) to nowhere",
            TextType.TEXT,
        )

        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Text with a ", TextType.TEXT),
                TextNode("nowhere", TextType.LINK, "http://localhost:8080"),
                TextNode(" to nowhere", TextType.TEXT),
            ],
            new_nodes,
        )
    
    def test_split_all_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("another link", TextType.LINK, "https://blog.boot.dev"),
                TextNode(" with text that follows", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes,
        )

if __name__ == "__main__":
    unittest.main()
