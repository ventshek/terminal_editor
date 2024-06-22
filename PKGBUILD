# Maintainer: Your Name <your.email@example.com>

pkgname=terminal_editor
pkgver=1.0
pkgrel=1
pkgdesc="A Powershell ISE bash clone"
arch=('x86_64')
url="https://example.com"
license=('MIT')
depends=('python' 'nuitka' 'gtk3' 'vte3')
source=('main.py')
md5sums=('SKIP')

build() {
    cd "$srcdir"
    nuitka3 --standalone --onefile --output-filename=terminal_editor main.py
}

package() {
    install -Dm755 "$srcdir/terminal_editor.bin" "$pkgdir/usr/bin/terminal_editor"
    install -Dm644 /dev/stdin "$pkgdir/usr/share/applications/terminal_editor.desktop" <<EOF
[Desktop Entry]
Name=terminal_editor
Comment=A Powershell ISE bash clone
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
