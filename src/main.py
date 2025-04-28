import os
import shutil
import sys

from block import markdown_to_html_node, extract_title
from parentnode import ParentNode

def main():
    root_path = "/"
    dst = "public"
    # print(sys.argv)
    if len(sys.argv) > 1:
        print("passed")
        dst = "docs"
        root_path = sys.argv[1]
    if os.path.exists(dst):
        shutil.rmtree(dst)
    copy_tree("static", dst)
    generate_page_recursively("content", "template.html", dst, root_path)

def generate_page_recursively(dir_path_content, template_path, dest_dir_path, basepath):
    dirs = os.listdir(dir_path_content)
    for directory_name in dirs:
        directory = os.path.join(dir_path_content, directory_name)
        dst_directory = os.path.join(dest_dir_path, directory_name)
        if os.path.isfile(directory) and directory_name[-3:] == ".md":
            dst_directory = dst_directory[:-3] + ".html"
            generate_page(directory, template_path, dst_directory, basepath)
            continue
        generate_page_recursively(directory, template_path, dst_directory, basepath)
    return

def copy_tree(src, dst):
    os.mkdir(dst)
    dirs = os.listdir(src)
    for directory_name in dirs:
        directory = os.path.join(src, directory_name)
        dst_directory = os.path.join(dst, directory_name)
        if os.path.isfile(directory):
            shutil.copy(directory, dst)
            continue
        copy_tree(directory, dst_directory)
    return

def generate_page(src_path, template_path, dst_path, basepath):
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
    output = output.replace('href="/', f'href="{basepath}')
    output = output.replace('src="/', f'src="{basepath}')
    # print(output)
    if os.path.exists(dst_path):
        os.remove(dst_path)
    paths = dst_path.split("/")
    if len(paths) > 2:
        make_paths = "/".join(paths[:-1])
        os.makedirs(make_paths)
    with open(dst_path, "w") as f:
        f.write(output)
        f.close()

if __name__ == "__main__":
    main()
