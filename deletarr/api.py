import requests
from functools import partial

from easypy.exceptions import PException
from easypy.bunch import Bunch

class TautulliAPI:
    class APIException(PException):
        pass

    def __init__(self, base_url, apikey) -> None:
        self.base_url = base_url
        self.apikey = apikey

    def _request(self, cmd, **kwargs) -> Bunch:
        params = f"apikey={self.apikey}&cmd={cmd}" + "".join(f"&{k}={v}" for (k, v) in kwargs.items())
        res = requests.get(f"{self.base_url}/api/v2?{params}").json()
        res = Bunch.from_dict(res)

        if res.response.result != "success":
            raise TautulliAPI.APIException(message=res.response.message)

        return res.response.data

    def __getattr__(self, cmd):
        return partial(self._request, cmd)