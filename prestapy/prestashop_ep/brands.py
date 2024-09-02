from typing import List

from .base import PsWebService, EndPointEnum


class Brand(PsWebService):
    def __init__(self, base_url, api_key=None):
        super().__init__(EndPointEnum.BRANDS, base_url, api_key)

    def get_active(self):
        manufacturers_params = {
            "display": "[id,name,active]",
            "filter[active]": 1
        }
        manufacturers_data = super().get_all(params=manufacturers_params)
        return {d['id']: d['name'] for d in manufacturers_data.get('manufacturers')}

    def get_products(self, manufacturer):
        pass
