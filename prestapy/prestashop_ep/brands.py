import random
import time

from .base import PsWebService, EndPointEnum
from .product import Product
from .stock import Stock


class Brand(PsWebService):
    def __init__(self, base_url=None, api_key=None):
        super().__init__(EndPointEnum.BRANDS, base_url, api_key)

    def get_active(self):
        manufacturers_params = {
            "display": "[id,name,active]",
            "filter[active]": 1
        }
        manufacturers_data = super().get_all(params=manufacturers_params)
        return {d['id']: d['name'] for d in manufacturers_data.get('manufacturers')}

    def get_products(self, brand, full_info=False, in_stock=True, without_images=False):
        products_ep = Product(base_url=self.url, api_key=self._api_key)
        stock_ep = Stock(base_url=self.url, api_key=self._api_key)

        manufacturers_params = {
            "filter[name]": brand
        }

        manufacturer_id = self.get_all(
            params=manufacturers_params
        )['manufacturers'][0]['id']

        limit = 100
        count = 0
        all_manufacturer_products = []

        if full_info:
            display = "full"
        else:
            display = "[id,reference,id_default_image]"

        while True:
            # print(f"Getting the products from {count * limit} to {(count + 1) * limit}")
            product_params = {
                "display": display,
                "filter[id_manufacturer]": manufacturer_id,
                "limit": f"{count * limit},{limit}"
            }

            res_data = products_ep.get_all(params=product_params)

            temp_products = res_data.get('products', []) if res_data else []

            all_manufacturer_products.extend(temp_products)

            if len(temp_products) < limit or len(temp_products) == 0:
                break
            else:

                time.sleep((random.random() * 4) + 1)
                count += 1
        if in_stock:
            stocks = stock_ep.stock_range()
            all_manufacturer_products = [product for product in all_manufacturer_products if
                                int(product['id']) in stocks]


        if without_images:
            all_manufacturer_products = [product for product in all_manufacturer_products if (product['id_default_image'] == "")]


        if full_info:
            categories = {}
            features = {}
            feature_values = {}
            products = []

            for product in all_manufacturer_products:
                reformated_product, new_categories, new_features, new_feature_values = products_ep.get_full_info(
                    product,
                    categories,
                    features,
                    feature_values
                )

                products.append(reformated_product)
                categories.update(new_categories)
                features.update(new_features)
                feature_values.update(new_features)
        else:
            products = [
                {
                    'id': pr.get('id'),
                    'reference': pr.get('reference')
                }
                for pr in all_manufacturer_products
            ]

        return products
