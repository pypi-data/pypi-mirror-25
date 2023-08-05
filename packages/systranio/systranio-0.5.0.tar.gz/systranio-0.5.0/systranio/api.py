"""
Base API
"""

import requests
from requests_toolbelt.multipart import decoder

from .exceptions import ParameterError, ApiKeyError, ApiFailure
from .utils import snake_to_camel_case

SYSTRANIO_URL = 'https://api-platform.systran.net'


class BaseAPI(object):
    """
    Base API class
    Subclasses all systran.io APIs (Translation, NLP, etc.)
    Calls are made with `requests`
    """
    key = ''
    payload = {}

    def __init__(self, key):
        """
        Sets the API Key
        Get yours on https://systran.io
        """
        self.key = key

    def _update_parameters(self, valid: dict, sent: dict) -> dict:
        """
        Validate a dict of parameters `sent` against a dict of `valid` ones
        Returns a dict of updated parameters or raise a ParameterError
        """
        invalid = [x for x in set(sent).difference(set(valid))]
        if invalid:
            raise ParameterError(', '.join(invalid))
        valid.update(sent)
        return valid

    def _call_url(self, endpoint: str) -> str:
        """
        Returns the full call url: host + endpoint
        """
        return '{}{}'.format(SYSTRANIO_URL, endpoint)

    def _handle_response(self, response: requests.Response):
        """
        Handles requests' response.
        * raises exceptions for status codes 400
        * tries to return json response or a multipart response (multipart form)
        * or an API failure
        """
        if response.status_code == 400:
            raise ApiKeyError('Invalid API key : {}'.format(self.key))
        if response.status_code == 200:
            try:
                return response.json()
            except ValueError:  # not json ? it must be a multipart response
                try:
                    multipart = decoder.MultipartDecoder.from_response(
                        response)
                    return multipart.parts
                except AttributeError:  # could be a string... like a translation.result()
                    return response.text
        try:
            result = response.json()
            raise ApiFailure(result['error']['message'])
        except ValueError:
            raise ApiFailure('Unknown error')

    @property
    def _camel_cased_payload(self):
        """
        converts snake_case_parameters to camelCasedOnes
        """
        return {snake_to_camel_case(k): v for k, v in self.payload.items()}

    def post(self, endpoint: str, files=None):
        """
        Sends a POST request to systran with all the parameters
        previously set.
        """
        self.payload.update(key=self.key)
        response = requests.post(
            self._call_url(endpoint),
            data=self._camel_cased_payload,
            files=files)
        self.payload.clear()
        return self._handle_response(response)

    def get(self, endpoint: str, headers=None):
        """
        Sends a GET request to systran with all the parameters
        previously set. Returns the json response or raises an exception
        """
        self.payload.update(key=self.key)
        headers = {
            'Accept': 'application/json',
        }
        response = requests.get(
            self._call_url(endpoint),
            params=self._camel_cased_payload,
            headers=headers)
        self.payload.clear()
        return self._handle_response(response)
