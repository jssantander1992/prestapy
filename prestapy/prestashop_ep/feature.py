from .base import PsWebService


class Feature(PsWebService):

    def __init__(self, base_url, api_key=None):
        super().__init__(PsWebService.EndPointEnum.FEATURES, base_url, api_key)

    def get_all(self, **kwargs):
        product_features_params = {
            "display": "[id,name]"
        }

        product_features = super().get_all(
            params=product_features_params
        )

        product_features_dict = {d['id']: d['name'] for d in product_features.get("product_features", [])}

        fs = FeatureValue(base_url=self._url)

        product_feature_values = fs.get_all()

        pf_with_key = [pf for pf in product_feature_values if int(
            pf["id_feature"]) in product_features_dict]
        pf_without_key = [pf for pf in product_feature_values if int(
            pf["id_feature"]) not in product_features_dict]
        pf_with_key = [{**pf, "name_feature": product_features_dict[int(pf['id_feature'])]} for pf in
                       pf_with_key]
        pf_without_key = [{**pf, "name_feature": None} for pf in
                          pf_without_key]
        product_feature_values = pf_with_key + pf_without_key
        product_feature_values_dict = {d['id']: {'value': d['value'], 'id_feature': d['id_feature'],
                                                 'name_feature': d['name_feature']} for d in
                                       product_feature_values}
        product_feature_values_dict = dict(
            sorted(product_feature_values_dict.items()))
        return product_feature_values_dict


class FeatureValue(PsWebService):

    def __init__(self, base_url, api_key=None):
        super().__init__(PsWebService.EndPointEnum.FEATURE_VALUES, base_url, api_key)

    def get_all(self, **kwargs):
        product_feature_values_params = {
            "display": "[id,id_feature,value]"
        }

        product_feature_values = super().get_all(
            params=product_feature_values_params
        )

        return product_feature_values.get("product_feature_values", [])
