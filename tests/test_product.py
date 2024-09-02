import os

from prestapy.prestashop_ep.product import Product


def test_product():
    url = os.environ.get('BASE_URL')
    f = Product(url)

    bs = f.get_all()
    print(bs)
    assert bs.__len__() > 0
