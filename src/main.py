import os

from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import HTMLNode, LeafNode
from copy_files import build
from generate_page import generate_pages_recursive

def main():
    build(os.path.abspath("./static/"), os.path.abspath("./public/"))
    generate_pages_recursive("./content","./template.html", "./public" )
    # generate_page("./content/index.md", "./template.html", os.path.join("./public", "index.html"))
    # generate_page("./content/blog/glorfindel/index.md", "./template.html", os.path.join("./public/blog/glorfindel", "index.html"))
    # generate_page("./content/blog/tom/index.md", "./template.html", os.path.join("./public/blog/tom", "index.html"))
    # generate_page("./content/blog/majesty/index.md", "./template.html", os.path.join("./public/blog/majesty", "index.html"))
    # generate_page("./content/contact/index.md", "./template.html", os.path.join("./public/contact", "index.html"))
if __name__ == "__main__":
    main()
