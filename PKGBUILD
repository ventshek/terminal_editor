# Maintainer: Your Name <your.email@example.com>
pkgname=my-python-package
pkgver=0.1.0
pkgrel=1
pkgdesc="A brief description of your package"
arch=('any')
url="https://github.com/yourusername/my-python-package"
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
}
