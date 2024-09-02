import os

from prestapy.prestashop_ep.brands import Brand


def test_brands():
    b = Brand()
    bs = b.get_products("CITIZEN")
    print(len(bs))
    assert bs.__len__() > 0
