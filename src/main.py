from textnode import TextNode
import os
import shutil


def copy_static_files(src: str, dst: str):
    # Step 1: If destination exists, delete it
    if os.path.exists(dst):
        shutil.rmtree(dst)

    # Step 2: Recreate the destination directory
    os.mkdir(dst)

    # Step 3: Recursive copy
    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)

        if os.path.isfile(src_path):
            shutil.copy(src_path, dst_path)
            print(f"Copied file: {src_path} -> {dst_path}")
        elif os.path.isdir(src_path):
            # Create directory then recursively copy
            os.mkdir(dst_path)
            print(f"Created directory: {dst_path}")
            copy_static_files(src_path, dst_path)


def main():
    copy_static_files("static", "public")


if __name__ == "__main__":
    main()
