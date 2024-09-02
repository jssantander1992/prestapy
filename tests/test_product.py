import os

from prestapy.prestashop_ep.product import Product


def test_product():
    f = Product()

    cats={}

    bs = f.get_missing_products("ARMANI EXCHANGE")
    print(bs)
    assert bs.__len__() > 0
