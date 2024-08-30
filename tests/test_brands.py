import os

from prestapy.prestashop_ep.brands import Brand


def test_brands():
    url = os.environ.get('BASE_URL')
    b = Brand(url)
    b_params = {
        'display':"[id,name]"
    }
    bs = b.get_all(params=b_params)
    print(bs)
    assert bs.__len__() > 0




