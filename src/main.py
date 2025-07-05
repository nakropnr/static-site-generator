import os
import shutil

from extract_title import generate_page


def main():
    shutil.rmtree("public")
    copy_recursive("static", "public")
    generate_page_recursive("content", "template.html", "public")


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

def generate_page_recursive(dir_path_content, template_path, dest_dir_path):
    content_list = os.listdir(path = dir_path_content)
    for file in content_list:
        full_path = os.path.join(dir_path_content, file)
        full_dest_path = os.path.join(dest_dir_path, file)
        dest_html_path = full_dest_path.replace(".md", ".html")
        if os.path.isfile(full_path):
            generate_page(full_path, template_path, dest_html_path)
        else:
            os.mkdir(dest_html_path)
            generate_page_recursive(full_path, template_path, dest_html_path)



if __name__ == "__main__":
    main()