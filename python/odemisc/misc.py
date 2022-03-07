
import os
import shutil

def rmandmkdir(dir):
    if os.path.exists(dir) & os.path.isfile(dir):
        os.remove(dir)
    if os.path.exists(dir) & os.path.isdir(dir):
        shutil.rmtree(dir)
    if not os.path.exists(dir):
        try:
            os.makedirs(dir)
        except :
            print(f"Error: directory {dir} create failed")
            exit()


