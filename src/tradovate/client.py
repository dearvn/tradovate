import os
from .session import TOSession
from .exceptions import handle_error_response, TOAPIError
from .config import URLs

def response_is_valid(resp):
    return resp.status_code in (200, 201, 204)


class TOClient(object):
    def __init__(self, user_id=None):
        self._userId = user_id or 1
        self.URL = URLs[os.getenv('TO_ENV')]
        self.session = TOSession(self._userId)

    def _request(self, url, method="GET", params=None, *args, **kwargs):
        url = f"{self.URL + url}"
        resp = self.session.request(method, self.URL.url, params=params, *args, **kwargs)
        if not response_is_valid(resp):
            handle_error_response(resp)
        return resp

    def _get(self, url, params=None, *args, **kwargs):
        url = f"{self.URL + url}"
        resp = self.session.request("GET", url, params=params, *args, **kwargs)
        if not response_is_valid(resp):
            handle_error_response(resp)
        return resp.json()

    def _post(self, url, params=None, *args, **kwargs):
        url = f"{self.URL + url}"
        resp = self.session.request("POST", url, params=params, *args, **kwargs)
        if not response_is_valid(resp):
            handle_error_response(resp)
        return resp.json()
