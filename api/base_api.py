import requests
from requests import Response, Session
from typing import Optional, Dict, Any


class BaseAPI:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self.session = Session()
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def _build_url(self, endpoint: str) -> str:
        return f"{self.base_url}/{endpoint.lstrip('/')}"

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None, **kwargs) -> Response:
        return self.session.get(self._build_url(endpoint), params=params, headers=self.headers, **kwargs)

    def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None, json: Optional[Dict[str, Any]] = None, **kwargs) -> Response:
        return self.session.post(self._build_url(endpoint), data=data, json=json, headers=self.headers, **kwargs)

    def put(self, endpoint: str, data: Optional[Dict[str, Any]] = None, **kwargs) -> Response:
        return self.session.put(self._build_url(endpoint), data=data, headers=self.headers, **kwargs)

    def patch(self, endpoint: str, data: Optional[Dict[str, Any]] = None, **kwargs) -> Response:
        return self.session.patch(self._build_url(endpoint), data=data, headers=self.headers, **kwargs)

    def delete(self, endpoint: str, **kwargs) -> Response:
        return self.session.delete(self._build_url(endpoint), headers=self.headers, **kwargs)

    def set_headers(self, headers: Dict[str, str]) -> None:
        self.headers.update(headers)

    def set_auth_token(self, token: str, scheme: str = "Bearer") -> None:
        self.headers["Authorization"] = f"{scheme} {token}"

    def close(self) -> None:
        self.session.close()
