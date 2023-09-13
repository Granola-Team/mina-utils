import shutil
import pathlib

HOME = pathlib.Path.home()
POSTGRES_SCRIPTS = pathlib.Path(__file__).parent
INCLUDE = POSTGRES_SCRIPTS / "include"

if __name__ == "__main__":
    # copy INCLUDE to HOME
    shutil.copytree(str(INCLUDE), str(HOME), dirs_exist_ok=True)
