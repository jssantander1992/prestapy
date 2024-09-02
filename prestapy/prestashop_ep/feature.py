from .base import PsWebService, EndPointEnum


class Feature(PsWebService):

    def __init__(self, base_url=None, api_key=None):
        super().__init__(EndPointEnum.FEATURES, base_url, api_key)


class FeatureValue(PsWebService):

    def __init__(self, base_url=None, api_key=None):
        super().__init__(EndPointEnum.FEATURE_VALUES, base_url, api_key)
