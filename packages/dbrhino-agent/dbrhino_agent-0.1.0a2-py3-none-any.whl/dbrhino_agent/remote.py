import requests


class Remote(object):
    def __init__(self, config):
        self.config = config

    def _request(self, method, path, headers={}, params={}, **kwargs):
        headers_ = self.config.remote_headers.copy()
        headers_.update(headers)
        return requests.request(method, self.config.remote_url(path),
                                headers=headers_, params=params, **kwargs)

    def upsert_databases(self):
        payload = [{"name": name} for name in self.config.databases]
        self._request("PUT", "/api/databases", json=payload)

    def fetch_grants(self):
        return self._request("GET", "/api/grants").json()
