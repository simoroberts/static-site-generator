from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes:list[TextNode], delimiter: str, text_type:TextType)-> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            split_nodes = []
            new_texts = node.text.split(delimiter)
            if (len(new_texts) % 2) == 0:
                raise Exception("Invalid Markdown Syntax")
            for i in range(0, len(new_texts)):
                if new_texts[i] == "":
                    continue
                split_nodes.append(TextNode(new_texts[i], TextType.TEXT if (i % 2) == 0 else text_type))
            new_nodes.extend(split_nodes)
    return new_nodes
