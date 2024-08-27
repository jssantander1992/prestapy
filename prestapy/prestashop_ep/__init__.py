import json
import os

import requests
from requests import HTTPError
from requests.auth import HTTPBasicAuth


class PSEndPoint:
    def __init__(self, base_url, endpoint, api_key=None):
        self._url = base_url
        self._base_endpoint = endpoint
        self._api_key = api_key if api_key is not None else os.environ.get('PSAPI_KEY')

    def get_url(self):

        return self._url

    @staticmethod
    def decode_data(content):
        match os.environ.get("DEFAULT_OUTPUT_FORMAT","JSON"):
            case "JSON":
                return json.loads(content)
            case _:
                return None

    def get_single(self, object_id, **kwargs):

        params = kwargs.get('params', {})

        params['output_format'] = os.environ.get("DEFAULT_OUTPUT_FORMAT") if "output_format" not in params else params[
            "output_format"]

        auth = HTTPBasicAuth(self._api_key, password='')

        r = requests.get(
            f'{self._url}/{self._base_endpoint}/{object_id}', auth=auth, params=params)

        r.raise_for_status()

        content = r.content

        return PSEndPoint.decode_data(content)

    def get_all(self, **kwargs):

        params = kwargs.get('params', {})

        params['output_format'] = os.environ.get("DEFAULT_OUTPUT_FORMAT","JSON") if "output_format" not in params else params[
            "output_format"]

        auth = HTTPBasicAuth(self._api_key, password='')


        r = requests.get(f'{self._url}/{self._base_endpoint}',
                         auth=auth, params=params)

        try:
            r.raise_for_status()
        except HTTPError as e:
            print(f"Error: {e}")
            return None
        content = r.content

        return PSEndPoint.decode_data(content)

    def create(self, data):
        pass

    def update(self, object_id, data):
        pass

    def delete(self, object_id):
        pass
