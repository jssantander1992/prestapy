from . import PSEndPoint


def get_features(url):
    product_features_ep = PSEndPoint(
        base_url=url, endpoint='api/product_features')
    product_features_params = {
        "display": "[id,name]"
    }

    product_features = product_features_ep.get_all(
        params=product_features_params)["product_features"]


    product_features_dict = {d['id']: d['name'] for d in product_features}
    product_feature_values_ep = PSEndPoint(
        base_url=url, endpoint="api/product_feature_values")
    product_feature_values_params = {
        "display": "[id,id_feature,value]"
    }

    product_feature_values = product_feature_values_ep.get_all(params=product_feature_values_params)[
        "product_feature_values"]

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
