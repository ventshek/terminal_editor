pkgname=terminal_editor
pkgver=1.0
pkgrel=1
pkgdesc="Powershell ISE bash clone"
arch=('x86_64')
url="https://github.com/ventshek/terminal_editor/tree/main"
license=('MIT')
depends=('python' 'gtk3' 'vte3')
makedepends=('nuitka' 'scons' 'base-devel')
source=("https://raw.githubusercontent.com/ventshek/terminal_editor/main/terminal_editor/main.py")
md5sums=('3646520c77917178a7ebd92171616424')
options=(!lto)

build() {
    cd "$srcdir"
    mkdir -p build
    cp main.py build/
    cd build
    nuitka3 --standalone --output-dir="$srcdir/build" --lto=no main.py
}

package() {
    cd "$srcdir/build"
    install -Dm755 main.dist/main.bin "$pkgdir/usr/bin/terminal_editor"
    
    # Install the data folder created by Nuitka's standalone mode
    cp -r main.dist/* "$pkgdir/usr/bin/"

    # Create .desktop file
    install -Dm644 /dev/stdin "$pkgdir/usr/share/applications/terminal_editor.desktop" <<EOF
[Desktop Entry]
Name=Terminal Editor
Comment=Powershell ISE bash clone
Exec=/usr/bin/terminal_editor
Icon=utilities-terminal
Terminal=false
Type=Application
Categories=Utility;
EOF
}

post_install() {
    update-desktop-database -q
}

post_remove() {
    update-desktop-database -q
}
