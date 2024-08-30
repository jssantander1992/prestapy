import os

import pytest

from prestapy.prestashop_ep.brands import get_manufacturers
from prestapy.prestashop_ep.product import get_full_info








def test_product():
    url = os.environ.get('BASE_URL')
    assert get_full_info(url, "CITIZEN").__len__() > 0
