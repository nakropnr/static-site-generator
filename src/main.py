import os
import shutil
import sys

from extract_title import extract_title
from markdown_to_html import markdown_to_html_node


def main():
    basepath = ""
    if len(sys.argv) <2:
        basepath = "/"
    else:
        basepath = sys.argv[1]
    shutil.rmtree("docs")
    copy_recursive("static", "docs")
    generate_page_recursive(basepath, "content", "template.html", "docs")


def copy_recursive(src_dir, dst_dir, is_root=True):
    if not os.path.exists(dst_dir) :
        os.mkdir(dst_dir)
    elif is_root == True:    
        shutil.rmtree(dst_dir)
        os.mkdir(dst_dir)
    file_list = os.listdir(path = src_dir)

    for file in file_list:
        full_path = os.path.join(src_dir, file)
        full_dst_path = os.path.join(dst_dir, file)
        print(f"Copying {full_path} -> {full_dst_path}")
        if os.path.isfile(full_path):
            shutil.copy(full_path, full_dst_path)
        else:
            copy_recursive(full_path, full_dst_path, is_root=False)

def generate_page_recursive(basepath, content_dir_path, template_path, dest_dir_path):
    content_list = os.listdir(path = content_dir_path)
    for file in content_list:
        full_path = os.path.join(content_dir_path, file)
        full_dest_path = os.path.join(dest_dir_path, file)
        dest_html_path = full_dest_path.replace(".md", ".html")
        if os.path.isfile(full_path):
            generate_page(basepath, full_path, template_path, dest_html_path)
        else:
            os.mkdir(dest_html_path)
            generate_page_recursive(basepath, full_path, template_path, dest_html_path)

def generate_page(basepath, content_dir_path, template_path, dest_path):
    print(f"Generating page from {content_dir_path} to {dest_path} using {template_path}")
    markdown_from = None
    markdown_template = None
    with open(content_dir_path, encoding="utf-8") as f:
        markdown_from = f.read()
    with open(template_path, encoding="utf-8") as f:
        markdown_template = f.read() 
    from_node = markdown_to_html_node(markdown_from).to_html()
    title = extract_title(markdown_from)

    title_replace = markdown_template.replace("{{ Title }}", title)
    content_replace = title_replace.replace("{{ Content }}", from_node)
    href_replace = content_replace.replace('href="/', f'href="{basepath}')
    src_replace = href_replace.replace('src="/', f'src="{basepath}')

    if not os.path.exists(dest_path):
        full_path = os.path.dirname(dest_path)
        os.makedirs(full_path, exist_ok=True)
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(src_replace)



if __name__ == "__main__":
    main()