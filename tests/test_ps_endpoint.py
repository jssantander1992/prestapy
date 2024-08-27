import pytest

from prestapy.prestashop_ep.brands import get_manufacturers
from prestapy.prestashop_ep.product import get_full_info

url = "https://s.scintilleshop.adlab.it/"
endpoint = 'api/manufacturers'


def test_brands():
    assert get_manufacturers(url).items().__len__() > 0


def test_product():
    assert get_full_info(url, "CITIZEN").__len__() > 0
