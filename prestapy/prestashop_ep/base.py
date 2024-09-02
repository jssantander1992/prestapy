import json
import os
from enum import Enum

import requests
from requests import HTTPError
from requests.auth import HTTPBasicAuth


class EndPointEnum(Enum):
    PRODUCTS = 'products'
    BRANDS = "manufacturers"
    CATEGORIES = "categories"
    FEATURES = "product_features"
    FEATURE_VALUES = "product_feature_values"
    STOCK_AVAILABLES = "stock_availables"


class PsWebService:

    def __init__(self, endpoint: EndPointEnum, base_url=None, api_key=None):

        self._url = base_url if base_url is not None else os.environ.get('BASE_URL')
        self._endpoint = endpoint
        self._api_key = api_key if api_key is not None else os.environ.get('PSAPI_KEY')
        self._auth = HTTPBasicAuth(self._api_key, password='')

    @property
    def endpoint(self):
        return self._endpoint

    @property
    def url(self):
        return self._url

    @property
    def api_key(self):
        return self._api_key

    @staticmethod
    def decode_data(content):
        match os.environ.get("DEFAULT_OUTPUT_FORMAT", "JSON"):
            case "JSON":
                return json.loads(content)
            case _:
                return None

    def get_single(self, object_id, **kwargs):

        params = kwargs.get('params', {})

        params['output_format'] = os.environ.get("DEFAULT_OUTPUT_FORMAT") if "output_format" not in params else params[
            "output_format"]
        url = f'{self._url}/api/{self._endpoint.value}/{object_id}'
        try:
            r = requests.get(url=url, auth=self._auth, params=params)

            r.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
            return None
        except Exception as err:
            print(f'An error occurred: {err}')

        content = r.content

        return PsWebService.decode_data(content)

    def get_all(self, **kwargs):

        params = kwargs.get('params', {})

        params['output_format'] = os.environ.get("DEFAULT_OUTPUT_FORMAT", "JSON") if "output_format" not in params else \
            params[
                "output_format"]

        url = f'{self._url}api/{self._endpoint.value}'
        try:
            r = requests.get(url, auth=self._auth, params=params)
            r.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
            return None
        except Exception as err:
            print(f'An error occurred: {err}')
            return None
        content = r.content

        return PsWebService.decode_data(content)

    def create(self, data):
        pass

    def update(self, object_id, data):
        pass

    def delete(self, object_id):
        pass
