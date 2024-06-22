rm -rf ./main.build
rm -rf ./main.dist
rm -rf ./main.onefile-build
nuitka3 --standalone --onefile --output-filename=terminal_editor main.py
rm -rf ./main.build
rm -rf ./main.dist
rm -rf ./main.onefile-build