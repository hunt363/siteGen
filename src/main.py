from block_nodes import markdown_to_html_node
from textnode import TextNode
import os
import shutil
import sys


def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise ValueError("No title found in markdown")


def generate_page(
    from_path: str, template_path: str, dest_path: str, basepath: str = "/"
):
    markdown = open(from_path, "r").read()
    template = open(template_path, "r").read()
    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    template = (
        template.replace("{{ Title }}", title)
        .replace("{{ Content }}", html)
        .replace('href="/', f'href="{basepath}')
        .replace('src="/', f'src="{basepath}')
    )
    open(dest_path, "w").write(template)


def generate_pages_recursive(
    dir_path_content: str, template_path: str, dest_dir_path: str, basepath: str = "/"
):
    if not os.path.exists(dest_dir_path):
        os.makedirs(dest_dir_path)
    for item in os.listdir(dir_path_content):
        item_path = os.path.join(dir_path_content, item)
        if item.endswith(".md"):
            dest_file_path = os.path.join(dest_dir_path, item.replace(".md", ".html"))
            generate_page(item_path, template_path, dest_file_path, basepath)
        elif os.path.isdir(item_path):
            new_dir_path = os.path.join(dest_dir_path, item)
            generate_pages_recursive(item_path, template_path, new_dir_path, basepath)


def copy_static_files(src: str, dst: str):
    if os.path.exists(dst):
        shutil.rmtree(dst)

    os.mkdir(dst)

    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)

        if os.path.isfile(src_path):
            shutil.copy(src_path, dst_path)
            print(f"Copied file: {src_path} -> {dst_path}")
        elif os.path.isdir(src_path):
            os.mkdir(dst_path)
            print(f"Created directory: {dst_path}")
            copy_static_files(src_path, dst_path)


def main():
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    copy_static_files("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath=basepath)


if __name__ == "__main__":
    main()
