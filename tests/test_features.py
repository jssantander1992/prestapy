import os

from prestapy.prestashop_ep.feature import Feature


def test_brands():
    url = os.environ.get('BASE_URL')
    f = Feature(url)

    bs = f.get_all()
    assert bs.__len__() > 0
