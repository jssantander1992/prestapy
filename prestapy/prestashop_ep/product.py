from .base import PsWebService, EndPointEnum
from .category import Category
from .feature import Feature, FeatureValue


class Product(PsWebService):
    def __init__(self, base_url=None, api_key=None):
        super().__init__(EndPointEnum.PRODUCTS, base_url, api_key)

    def get_full_info(self, product2refactor, categories=None, features=None, feature_values=None):
        if categories is None:
            categories = {}
        if features is None:
            features = {}
        if feature_values is None:
            feature_values = {}

        categories, category_default, other_categories = self._get_categories(product2refactor, categories)

        features, feature_values, pr_features = self._get_features(product2refactor, features, feature_values)

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

            "default_category": category_default,
            "other_categories": other_categories,
            "features": pr_features,
            'images': product2refactor.get('associations', {}).get('images', []),

        }

        return new_product, categories, features, feature_values

    def _get_categories(self, product2refactor, categories=None):
        if categories is None:
            categories = {}

        init_categories = product2refactor.get("associations", {}).get("categories", [])
        id_category_default = product2refactor.get('id_category_default', None)
        categories, pr_categories = self._update_categories(init_categories, categories)
        category_default = pr_categories.pop(id_category_default, {})
        other_categories = pr_categories

        return categories, category_default, other_categories

    def _update_categories(self, pr_categories, categories=None):
        if categories is None:
            categories = {}

        new_categories_ids = [cat.get('id') for cat in pr_categories if int(cat.get('id')) not in categories]
        category_ep = Category()
        cat_params = {
            "filter[id]": f"[{'|'.join(new_categories_ids)}]"
        }
        new_categories = category_ep.get_all(params=cat_params) if new_categories_ids else {}
        categories = {**categories, **new_categories}
        pr_categories = {cat.get('id'): categories.get(int(cat.get('id'))) for cat in pr_categories}

        return categories, pr_categories

    def _get_features(self, product2refactor, features=None, feature_values=None):
        if features is None:
            features = {}
        if feature_values is None:
            feature_values = {}

        init_features = product2refactor.get("associations", {}).get("product_features", [])

        features = self._update_features(init_features, features)
        feature_values = self._update_feature_values(init_features, feature_values)

        pr_features = [
            {
                "value": feature_values.get(int(feat.get("id_feature_value"))),
                "id_feature": feat.get("id"),
                "name_feature": features.get(int(feat.get("id"))),
            } for feat in init_features
        ]

        return features, feature_values, pr_features

    def _update_features(self, pr_features, features=None):
        if features is None:
            features = {}

        feature_ep = Feature()

        pr_features_ids = [feat.get('id') for feat in pr_features]
        new_features_ids = [feat for feat in pr_features_ids if int(feat) not in features]

        feat_params = {
            "display": "[id,name]",
            "filter[id]": f"[{'|'.join(new_features_ids)}]"
        }

        new_features = feature_ep.get_all(params=feat_params).get("product_features", []) if new_features_ids else []
        refactor_features = {feat.get("id"): feat.get("name") for feat in new_features}

        features = {**features, **refactor_features}
        return features

    def _update_feature_values(self, pr_features, feature_values):
        if feature_values is None:
            feature_values = {}

        feature_value_ep = FeatureValue()

        pr_features_ids = [feat.get('id_feature_value') for feat in pr_features]
        new_features_ids = [feat for feat in pr_features_ids if int(feat) not in feature_values]

        feat_params = {
            "display": "[id,value]",
            "filter[id]": f"[{'|'.join(new_features_ids)}]"
        }

        new_features = feature_value_ep.get_all(params=feat_params).get("product_feature_values",
                                                                        []) if new_features_ids else []
        refactor_features = {feat.get("id"): feat.get("value") for feat in new_features}

        feature_values = {**feature_values, **refactor_features}

        return feature_values
