import os
import pathlib

def read(fpath: pathlib.Path) ->  str:
    contents = ""
    if fpath.exists():
        contents = fpath.read_text()
    return contents

def mkdir(dir_path: pathlib.Path):
    '''
    Creates the dir if it doesn't already exist
    '''
    if not dir_path.exists():
        os.system(f"mkdir {dir_path}")

def mkdir_rec(main_dir_path: pathlib.Path):
    '''
    Creates the dir path to `main_dir_path` starting from the deepest one not in existence
    '''
    parents = main_dir_path.parents
    for dir_path in parents:
        mkdir(dir_path)

def write(fpath: pathlib.Path, contents: str = ""):
    '''
    Make dir path and write `contents` to `fpath`
    '''
    if not fpath.parent.exists():
        mkdir_rec(fpath.parent)
    if not fpath.exists():
        os.system(f"touch {fpath}")
    else:
        os.unlink(str(fpath))
    fpath.write_text(contents)
