import re
from textnode import TextNode, TextType

# IMAGE_PATTERN = r"!\[(.*?)\]\((.*?)\)"
IMAGE_PATTERN = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
# LINK_PATTERN = r"\[(.*?)\]\((.*?)\)"
LINK_PATTERN = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"

def extract_markdown_images(text: str):
    return re.findall(IMAGE_PATTERN, text)

def extract_markdown_links(text: str):
    return re.findall(LINK_PATTERN, text)

def split_nodes_delimiter(old_nodes:list[TextNode], delimiter: str, text_type:TextType)-> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            split_nodes = []
            sections = node.text.split(delimiter)
            if (len(sections) % 2) == 0:
                raise Exception("Invalid Markdown Syntax")
            for i in range(0, len(sections)):
                if sections[i] == "":
                    continue
                split_nodes.append(TextNode(sections[i], TextType.TEXT if (i % 2) == 0 else text_type))
            new_nodes.extend(split_nodes)
    return new_nodes

# def link_loop(text_to_split:str, alt:str, url:str)->list:

#     pass

def split_nodes_image(old_nodes) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            split_nodes = []
            image_tuples = extract_markdown_images(node.text)
            original_text = node.text
            if len(image_tuples) < 1:
                new_nodes.append(node)
                continue

            for tag, url in image_tuples:
                sections = original_text.split(f"![{tag}]({url})", 1)
                if len(sections) != 2:
                    raise ValueError("Invalid markdown, image section not closed")
                if sections[0] != "":
                    split_nodes.append(TextNode(sections[0], TextType.TEXT))
                split_nodes.append(TextNode(tag, TextType.IMAGE, url=url))
                original_text = sections[-1]

            if original_text != "":
                split_nodes.append(TextNode(original_text, TextType.TEXT))

            new_nodes.extend(split_nodes)
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            split_nodes = []
            link_tuples = extract_markdown_links(node.text)
            original_text = node.text
            if len(link_tuples) < 1:
                new_nodes.append(node)
                continue

            for tag, url in link_tuples:
                sections = original_text.split(f"[{tag}]({url})", 1)
                if len(sections) != 2:
                    raise ValueError("Invalid markdown, link section not closed")
                if sections[0] != "":
                    split_nodes.append(TextNode(sections[0], TextType.TEXT))
                split_nodes.append(TextNode(tag, TextType.LINK, url=url))
                original_text = sections[-1]
            
            if original_text != "":
                split_nodes.append(TextNode(original_text, TextType.TEXT))
            
            new_nodes.extend(split_nodes)
            
    return new_nodes

def text_to_textnodes(text:str)->list[TextNode]:
    nodes:list[TextNode] = [TextNode(text, TextType.TEXT)]
    nodes = (split_nodes_delimiter(nodes, "**", TextType.BOLD))
    nodes = (split_nodes_delimiter(nodes, "_", TextType.ITALIC))
    nodes = (split_nodes_delimiter(nodes, "`", TextType.CODE))
    nodes = (split_nodes_image(nodes))
    nodes = (split_nodes_link(nodes))
    return nodes
