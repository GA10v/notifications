import requests
from generator.src.utils.auth import get_access_token


class AuthenticatedSession:
    def __init__(self) -> None:
        self.session = requests.Session()
        self._set_auth_header()

    def _set_auth_header(self) -> None:
        _token = get_access_token()
        self.session.headers.update({'Authorization': f'Bearer {_token}'})

    def get(self, url, **kwargs) -> requests.Response:  # type: ignore[no-untyped-def]
        return self.session.get(url=url, **kwargs)

    def post(self, url, payload=None, **kwargs) -> requests.Response:  # type: ignore[no-untyped-def]
        return self.session.post(url=url, data=payload, **kwargs)

    def close(self) -> None:
        self.session.close()
