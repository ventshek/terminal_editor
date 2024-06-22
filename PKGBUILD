# Maintainer: Your Name <your.email@example.com>

pkgname=terminal_editor
pkgver=1.0
pkgrel=1
pkgdesc="Powershell ISE bash clone"
arch=('x86_64')
url="https://example.com"
license=('MIT')
depends=('python' 'gtk3' 'vte3')
makedepends=('nuitka')
source=('main.py::https://raw.githubusercontent.com/ventshek/terminal_editor/main/terminal_editor/main.py')
md5sums=('SKIP')

build() {
    cd "$srcdir"
    nuitka --standalone --onefile --output-filename=terminal_editor main.py
}

package() {
    install -Dm755 "$srcdir/myscript.dist/terminal_editor" "$pkgdir/usr/bin/terminal_editor"
    
    # Create .desktop file
    install -Dm644 /dev/stdin "$pkgdir/usr/share/applications/terminal_editor.desktop" <<EOF
[Desktop Entry]
Name=terminal_editor
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
