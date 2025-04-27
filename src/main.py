import os
import shutil

def main():
    if os.path.exists("public"):
        shutil.rmtree("public")
    copy_tree("static", "public")

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

if __name__ == "__main__":
    main()
