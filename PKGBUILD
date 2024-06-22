# Maintainer: Your Name <ventshek@gmail.com>
pkgname=terminal_editor
pkgver=1.0
pkgrel=1
pkgdesc="A Powershell ISE Bash clone"
arch=('any')
url="https://github.com/ventshek/terminal_editor"
license=('GPL')
depends=('gtk3' 'vte3' 'python' 'gobject-introspection')
makedepends=('python-setuptools')
source=("$pkgname-$pkgver.tar.gz::https://github.com/yourusername/$pkgname/archive/refs/tags/v$pkgver.tar.gz")
sha256sums=('SKIP')

build() {
    cd "$srcdir/$pkgname-$pkgver"
    python setup.py build
}

package() {
    cd "$srcdir/$pkgname-$pkgver"
    python setup.py install --root="$pkgdir/" --optimize=1
    install -Dm644 terminal_editor.desktop "$pkgdir/usr/share/applications/terminal_editor.desktop"
}

post_remove() {
    rm -f "/usr/share/applications/terminal_editor.desktop"
}