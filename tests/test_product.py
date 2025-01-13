import os

from prestapy.prestashop_ep.product import Product


def test_product():
    url = os.environ.get('BASE_URL')
    f = Product(url)

    bs = f.get_all()
    print(bs)
    assert bs.__len__() > 0


def test_product_full_info():
    url = os.environ.get('BASE_URL')
    f = Product(url)
    bs = f.get_single(519291)
    print(bs)
    assert bs.__len__() > 0
