import os
from block_markdown import markdown_to_blocks, markdown_to_html_node

def extract_title(markdown:str) -> str:
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block.startswith("# "):
            return block[2:]
    raise ValueError("Markdown missing Title Header")

def generate_page(from_path:str, template_path:str, dest_path:str) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown = ""
    with open(from_path, "r") as fd:
        markdown = fd.read()
    template = ""
    with open(template_path, "r") as fd:
        template = fd.read()

    title = extract_title(markdown)
    content = markdown_to_html_node(markdown).to_html()

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", content)
    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    with open(dest_path, "w") as fd:
        fd.write(template)

def generate_pages_recursive(dir_path_content:str, template_path:str, dest_dir_path:str) -> None:
    for file in os.listdir(dir_path_content):
        filepath = os.path.join(dir_path_content, file)
        if os.path.isdir(filepath):
            generate_pages_recursive(filepath, template_path, os.path.join(dest_dir_path, file))
        else:
            generate_page(filepath, template_path, os.path.join(dest_dir_path, "index.html"))
