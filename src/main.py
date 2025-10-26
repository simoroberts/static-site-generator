import os

from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import HTMLNode, LeafNode
from copy_files import build
from generate_page import generate_page

def main():
    build(os.path.abspath("./static/"), os.path.abspath("./public/"))
    generate_page("./content/index.md", "./template.html", os.path.join("./public", "index.html"))
if __name__ == "__main__":
    main()
