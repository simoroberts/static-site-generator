from __future__ import annotations
from typing import Annotated
from enum import Enum

from htmlnode import HTMLNode, ParentNode, LeafNode
class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    """
    Represents a text node for conversion from Markdown to HTML
    Attributes:
        text (str): The text of the node
        text_type (TextType): The type of text the node is
        url (str|None): The url of the node if it is an image or link
    """
    def __init__(self, text:str, text_type:TextType, url:str|None=None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other: object, /) -> bool:
        if not isinstance(other, TextNode):
            return NotImplemented
        if self.text == other.text and self.text_type == other.text_type and self.url == other.url:
            return True
        return False

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def text_node_to_html_node(text_node: TextNode) -> HTMLNode:
    match(text_node.text_type):
        case TextType.TEXT: 
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            if text_node.url is None:
                raise ValueError("Link URL Empty")
            return LeafNode("a", text_node.text, props={"href": text_node.url})
        case TextType.IMAGE:
            if text_node.url is None:
                raise ValueError("Image src Empty")
            return LeafNode("img", "", props={"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError(f"Invalid TextType: {text_node.text_type}")

    raise ValueError(f"Invalid TextType: {text_node.text_type}")
