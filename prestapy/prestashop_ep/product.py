import random
import time

from .base import PsWebService
from .brands import Brand
from .category import Category
from .feature import Feature
from .stock import Stock


class Product(PsWebService):
    def __init__(self, base_url, api_key=None):
        super().__init__(PsWebService.EndPointEnum.PRODUCTS, base_url, api_key)

    def get_missing_products(self, brand):
        manufacturers_ep = Brand(base_url=self.url, api_key=self._api_key)
        stock_ep = Stock(base_url=self.url, api_key=self._api_key)
        category_ep = Category(base_url=self.url, api_key=self._api_key)
        feature_ep = Feature(base_url=self.url, api_key=self._api_key)


        manufacturers_params = {
            "filter[name]": brand
        }

        manufacturer_id = manufacturers_ep.get_all(
            params=manufacturers_params
        )['manufacturers'][0]['id']

        stocks = stock_ep.stock_range()

        limit = 100
        count = 0
        all_manufacturer_products = []

        while True:
            # print(f"Getting the products from {count * limit} to {(count + 1) * limit}")
            product_params = {
                "display": "full",
                "filter[id_manufacturer]": manufacturer_id,
                "limit": f"{count * limit},{limit}"
            }

            res_data = super().get_all(params=product_params)

            temp_products = res_data.get('products', []) if res_data else []

            all_manufacturer_products.extend(temp_products)

            if len(temp_products) < limit or len(temp_products) == 0:
                break
            else:

                time.sleep((random.random() * 4) + 1)
                count += 1

        missing_products = [product for product in all_manufacturer_products if
                            (product['id_default_image'] != "") and int(product['id']) in stocks]

        categories = category_ep.get_all()

        features = feature_ep.get_all()

        def product_refactor(product2refactor):
            id_category_default = int(product2refactor['id_category_default'])

            all_categories = product2refactor['associations']['categories'] \
                if 'associations' in product2refactor and "categories" in product2refactor['associations'] \
                else []

            all_features = product2refactor['associations']['product_features'] \
                if 'associations' in product2refactor and "product_features" in product2refactor['associations'] \
                else []

            all_id_features = [int(feature.get('id_feature_value')) for feature in all_features]

            parsed_features = [features.get(feature) for feature in all_id_features]

            all_categories = [int(category.get('id')) for category in all_categories]
            all_categories = [category for category in all_categories if category != id_category_default]

            category_default = categories.get(id_category_default, {})

            other_categories = [categories.get(category) for category in all_categories]

            new_product = {
                "item_id": product2refactor['id'],
                "reference": product2refactor['reference'],
                "manufacturer_name": product2refactor['manufacturer_name'],
                "id_default_image": product2refactor['id_default_image'],

                "name": product2refactor["name"],
                "meta_description": product2refactor["meta_description"],
                "meta_keywords": product2refactor["meta_keywords"],
                "meta_title": product2refactor["meta_title"],
                "link_rewrite": product2refactor["link_rewrite"],
                "description": product2refactor["description"],
                "description_short": product2refactor["description_short"],
                "price": float(product2refactor["price"]),
                "tax_price": float(product2refactor["price"]) * 1.22,
                "date_upd": product2refactor["date_upd"],

                "default_category_id": id_category_default,
                "other_categories_id": all_categories,

                "default_category": category_default,
                "other_categories": other_categories,
                "features": parsed_features,
                'images': product2refactor.get('associations', {}).get('images', []),

            }
            return new_product

        products = [product_refactor(product) for product in missing_products]

        return products
