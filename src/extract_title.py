import os
from markdown_to_html import markdown_to_html_node


def extract_title(markdown):
    if markdown.startswith("#"):
        extracted = markdown.strip("# ")
    else:
        raise Exception("Not header!")
    return extracted

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown_from = None
    markdown_template = None
    with open(from_path, encoding="utf-8") as f:
        markdown_from = f.read()
    with open(template_path, encoding="utf-8") as f:
        markdown_template = f.read() 
    from_node = markdown_to_html_node(markdown_from).to_html()
    template_node = markdown_to_html_node(markdown_template).to_html()
    title = extract_title(markdown_from)

    title_replace = markdown_template.replace("{{ Title }}", title)
    content_replace = title_replace.replace("{{ Content }}", from_node)

    if not os.path.exists(dest_path):
        full_path = os.path.dirname(dest_path)
        os.makedirs(full_path, exist_ok=True)
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(content_replace)