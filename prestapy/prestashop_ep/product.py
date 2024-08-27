import random
import time

from . import PSEndPoint
from .category import get_categories
from .feature import get_features
from .stock import get_stocks


def get_full_info(url, manufacturer, min_quantity=1, max_quantity=600):
    manufacturers_ep = PSEndPoint(base_url=url, endpoint='api/manufacturers')
    manufacturers_params = {
        "filter[name]": manufacturer
    }
    # print(manufacturers_ep.get_all(params=manufacturers_params))
    manufacturer_id = manufacturers_ep.get_all(params=manufacturers_params)[
        'manufacturers'][0]['id']

    stocks = get_stocks(url, min_quantity, max_quantity)

    limit = 100
    count = 0
    all_manufacturer_products = []
    product_ep = PSEndPoint(base_url=url, endpoint='api/products')

    while True:
        # print(f"Getting the products from {count * limit} to {(count + 1) * limit}")
        product_params = {
            "display": "full",
            "filter[id_manufacturer]": manufacturer_id,
            "limit": f"{count * limit},{limit}"
        }

        temp_products = product_ep.get_all(
            params=product_params)["products"]

        all_manufacturer_products.extend(temp_products)

        if len(temp_products) < limit:
            break
        else:

            time.sleep((random.random() * 4) + 1)
            count += 1

    missing_products = [product for product in all_manufacturer_products if
                        (product['id_default_image'] != "") and int(product['id']) in stocks]

    categories = get_categories(url)

    features = get_features(url)

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
