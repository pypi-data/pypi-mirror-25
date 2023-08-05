import requests


class Remote(object):
    def __init__(self, config):
        self.config = config

    def _request(self, method, path, headers={}, params={}, **kwargs):
        headers_ = self.config.remote_headers.copy()
        headers_.update(headers)
        params_ = self.config.remote_params.copy()
        params_.update(params)
        return requests.request(method, self.config.remote_url(path),
                                headers=headers_, params=params_, **kwargs)

    def upsert_databases(self):
        payload = [{"name": name} for name in self.config.databases]
        self._request("PUT", "/api/databases", json=payload)

    def fetch_grants(self):
        response = self._request("GET", "/api/grants")
        return response.json()["grants"]
