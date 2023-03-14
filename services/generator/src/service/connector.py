import requests


class AuthenticatedSession:
    def __init__(
        self,
        auth_token: str,
        host: str = '0.0.0.0',
        port: int = 8081,
    ):
        self.auth_token = auth_token
        self.host = host
        self.port = port
        self.session = requests.Session()
        self._set_auth_header()

    def _set_auth_header(self):
        self.session.headers.update({'Authorization': f'Bearer {self.auth_token}'})

    def get(self, url, **kwargs):
        return self.session.get(f'{self.host}:{self.port}{url}', **kwargs)

    def post(self, url, payload=None, **kwargs):
        return self.session.post(f'{self.host}:{self.port}{url}', data=payload, **kwargs)

    def close(self):
        self.session.close()
