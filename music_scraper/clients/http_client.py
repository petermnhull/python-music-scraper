import requests
from typing import Dict


USER_AGENT = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0"


class HTTPClient:
    @staticmethod
    def _merge_maps(a: Dict, b: Dict) -> Dict:
        for k, v in a.items():
            b[k] = v
        return b

    def _enhance_headers(self, headers: Dict) -> Dict:
        additional = requests.utils.default_headers()
        additional["User-Agent"] = USER_AGENT
        return self._merge_maps(headers, additional)

    def do_get(self, url: str, headers: Dict = {}) -> requests.Response:
        response = requests.get(url, headers=self._enhance_headers(headers))
        return response

    def do_post(
        self, url: str, body: Dict = {}, headers: Dict = {}, auth=None
    ) -> requests.Response:
        response = requests.post(url, headers=self._enhance_headers(headers), data=body, auth=auth)
        return response
