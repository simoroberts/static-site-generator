from __future__ import annotations
from enum import Enum

from htmlnode import HTMLNode, ParentNode
from inline_markdown import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unorderd_list"
    OLIST = "ordered_list"

def markdown_to_blocks(markdown:str) -> list[str]:
    return [block.strip() for block in markdown.split("\n\n") if block != ""]

def block_to_block_type(block:str) -> BlockType:
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    
    lines = block.split("\n")
    for line in lines:
        if not line.startswith(">"):
            break
        return BlockType.QUOTE

    for line in lines:
        if not line.startswith("- "):
            break
        return BlockType.ULIST

    for i in range(len(lines)):
        if not lines[i].startswith(f"{i+1}. "):
            break
        return BlockType.OLIST
    
    return BlockType.PARAGRAPH

# def text_to_children(text:str) -> list[HTMLNode]:
#     text_nodes = text_to_textnodes(text.replace("\n", " "))
#     return [text_node_to_html_node(node) for node in text_nodes]

# def code_to_children(text:str) -> list[HTMLNode]:
#     t1 = text[4:-3]
#     text_node = TextNode(t1, TextType.TEXT)
#     child = text_node_to_html_node(text_node)

#     return [ParentNode("code", [child])]
#     

# def get_heading_tag(text:str) -> str:
#     if text.startswith("######"):
#         return "h6"
#     if text.startswith("#####"):
#         return "h5"
#     if text.startswith("####"):
#         return "h4"
#     if text.startswith("###"):
#         return "h3"
#     if text.startswith("##"):
#         return "h2"
#     if text.startswith("#"):
#         return "h1"
#     return ""

# def markdown_to_html_node(markdown:str) -> HTMLNode:
#     root = ParentNode("div", [], None)
#     blocks = markdown_to_blocks(markdown)
#     children = []
#     for block in blocks:
#         node = None
#         match block_to_block_type(block):
#             case BlockType.PARAGRAPH:
#                 node = ParentNode("p", text_to_children(block), None)
#             case BlockType.HEADING:
#                 node = ParentNode(get_heading_tag(block), text_to_children(block), None)
#             case BlockType.CODE:
#                 node = ParentNode("pre", code_to_children(block), None)
#             case BlockType.QUOTE:
#                 node = ParentNode("blockquote", text_to_children(block), None)
#             case BlockType.ULIST:
#                 node = ParentNode("ul", text_to_children(block), None)
#             case BlockType.OLIST:
#                 node = ParentNode("ol", text_to_children(block), None)
#         if node is None:
#             continue
#         children.append(node)
#     
#     root.children = children
#     return root

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.OLIST:
        return olist_to_html_node(block)
    if block_type == BlockType.ULIST:
        return ulist_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    raise ValueError("invalid block type")


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])


def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)
