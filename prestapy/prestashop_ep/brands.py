from . import PSEndPoint


def get_manufacturers(url, api_key=None):
    manufacturers_ep = PSEndPoint(base_url=url, endpoint='api/manufacturers', api_key=api_key)
    manufacturers_params = {
        "display": "[id,name,active]",
        "filter[active]": 1
    }
    manufacturers_data = manufacturers_ep.get_all(
        params=manufacturers_params)["manufacturers"]
    manufacturers = {d['id']: d['name'] for d in manufacturers_data}
    return manufacturers
