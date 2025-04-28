import os
import shutil

from block import markdown_to_html_node, extract_title
from parentnode import ParentNode

def main():
    if os.path.exists("public"):
        shutil.rmtree("public")
    copy_tree("static", "public")
    generate_page("content/index.md", "template.html", "public/index.html")

def copy_tree(src, dst):
    os.mkdir(dst)
    dirs = os.listdir(src)
    for directory_name in dirs:
        directory = os.path.join(src, directory_name)
        dst_directory = os.path.join(dst, directory_name)
        if os.path.isfile(directory):
            shutil.copy(directory, dst)
            return
        copy_tree(directory, dst_directory)

def generate_page(src_path, template_path, dst_path):
    print(f"Generating page from {src_path} to {dst_path} using {template_path}")
    markdown = ""
    template = ""
    with open(src_path) as f:
        markdown = f.read()
        f.close()
    with open(template_path) as f:
        template = f.read()
        f.close()
    nodes = markdown_to_html_node(markdown)
    content = nodes.to_html()
    title = extract_title(markdown)
    # print(content)
    output = template.replace("{{ Title }}", title)
    output = output.replace("{{ Content }}", content)
    # print(output)
    if os.path.exists(dst_path):
        os.remove(dst_path)
    # os.makedirs(dst_path)
    with open(dst_path, "w") as f:
        f.write(output)
        f.close()

if __name__ == "__main__":
    main()
