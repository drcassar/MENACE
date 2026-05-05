import pathlib
import os

# Resolve asset paths relative to the installed package directory
_pkg_dir = pathlib.Path(__file__).parent
os.chdir(_pkg_dir)

from menace_jogo.main import main

if __name__ == "__main__":
    main()
