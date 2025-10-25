from __future__ import annotations
from typing import Annotated
from enum import Enum

class TextType(Enum):
    PLAIN = "plain"
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
