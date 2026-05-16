import logging
import time
from typing import Any, Dict, List, Optional

from requests import Response, Session
from requests.exceptions import ConnectionError, Timeout

logger = logging.getLogger(__name__)


class ApiClientError(Exception):
    """Raised when an API response indicates failure."""

    def __init__(self, status_code: int, body: Any, message: str = ""):
        self.status_code = status_code
        self.body = body
        self.message = message or f"API request failed with status {status_code}"
        super().__init__(self.message)


class ApiClient:
    """Reusable HTTP client with logging, retry, and response validation.

    Wraps a requests.Session and provides typed helpers for
    GET, POST, PUT, PATCH, and DELETE.
    """

    def __init__(
        self,
        base_url: str = "",
        timeout: int = 30,
        retry_count: int = 0,
        retry_delay: float = 1.0,
        headers: Optional[Dict[str, str]] = None,
    ):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.retry_count = retry_count
        self.retry_delay = retry_delay
        self.session = Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json",
            **(headers or {}),
        })
        self._request_id = 0

    # ── Public HTTP Methods ───────────────────────────────────────

    def get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs: Any,
    ) -> Response:
        return self._request("GET", endpoint, params=params, headers=headers, **kwargs)

    def post(
        self,
        endpoint: str,
        json: Optional[Dict[str, Any]] = None,
        data: Any = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs: Any,
    ) -> Response:
        return self._request("POST", endpoint, json=json, data=data, headers=headers, **kwargs)

    def put(
        self,
        endpoint: str,
        json: Optional[Dict[str, Any]] = None,
        data: Any = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs: Any,
    ) -> Response:
        return self._request("PUT", endpoint, json=json, data=data, headers=headers, **kwargs)

    def patch(
        self,
        endpoint: str,
        json: Optional[Dict[str, Any]] = None,
        data: Any = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs: Any,
    ) -> Response:
        return self._request("PATCH", endpoint, json=json, data=data, headers=headers, **kwargs)

    def delete(
        self,
        endpoint: str,
        headers: Optional[Dict[str, str]] = None,
        **kwargs: Any,
    ) -> Response:
        return self._request("DELETE", endpoint, headers=headers, **kwargs)

    # ── Response Helpers ──────────────────────────────────────────

    @staticmethod
    def raise_for_status(response: Response) -> None:
        """Raise ApiClientError if the response status is not 2xx."""
        if response.ok:
            return
        body: Any = ""
        try:
            body = response.json()
        except Exception:
            body = response.text
        raise ApiClientError(response.status_code, body)

    @staticmethod
    def json_body(response: Response) -> Any:
        ApiClient.raise_for_status(response)
        try:
            return response.json()
        except ValueError as exc:
            raise ApiClientError(
                response.status_code,
                response.text,
                f"Response body is not valid JSON: {exc}",
            ) from exc

    @staticmethod
    def json_list(response: Response) -> List[Any]:
        data = ApiClient.json_body(response)
        if not isinstance(data, list):
            raise ApiClientError(
                response.status_code,
                data,
                f"Expected JSON array, got {type(data).__name__}",
            )
        return data

    @staticmethod
    def json_dict(response: Response) -> Dict[str, Any]:
        data = ApiClient.json_body(response)
        if not isinstance(data, dict):
            raise ApiClientError(
                response.status_code,
                data,
                f"Expected JSON object, got {type(data).__name__}",
            )
        return data

    @staticmethod
    def status_ok(response: Response) -> bool:
        return response.ok

    # ── Headers ───────────────────────────────────────────────────

    def set_header(self, key: str, value: str) -> "ApiClient":
        self.session.headers[key] = value
        return self

    def set_auth_token(self, token: str, scheme: str = "Bearer") -> "ApiClient":
        self.session.headers["Authorization"] = f"{scheme} {token}"
        return self

    def set_base_url(self, url: str) -> "ApiClient":
        self.base_url = url.rstrip("/")
        return self

    # ── Lifecycle ─────────────────────────────────────────────────

    def close(self) -> None:
        self.session.close()

    # ── Internal ──────────────────────────────────────────────────

    def _build_url(self, endpoint: str) -> str:
        if endpoint.startswith("http://") or endpoint.startswith("https://"):
            return endpoint
        return f"{self.base_url}/{endpoint.lstrip('/')}"

    def _log_request(self, method: str, url: str, **kwargs: Any) -> int:
        self._request_id += 1
        rid = self._request_id
        log_payload = {}
        if kwargs.get("json"):
            log_payload["json"] = kwargs["json"]
        if kwargs.get("params"):
            log_payload["params"] = kwargs["params"]
        msg = f"[{rid}] {method} {url}"
        if log_payload:
            msg += f" | {log_payload}"
        logger.debug(msg)
        return rid

    def _log_response(self, rid: int, response: Response, elapsed: float) -> None:
        logger.debug(
            "[%d] <- %s %s | %s | %.3fs",
            rid,
            response.status_code,
            response.reason,
            len(response.content),
            elapsed,
        )

    def _request(self, method: str, endpoint: str, **kwargs: Any) -> Response:
        url = self._build_url(endpoint)
        merged_headers = {**self.session.headers, **(kwargs.pop("headers", {}))}
        kwargs.setdefault("timeout", self.timeout)
        kwargs["headers"] = merged_headers

        rid = self._log_request(method, url, **kwargs)
        last_error: Optional[Exception] = None

        for attempt in range(self.retry_count + 1):
            try:
                start = time.monotonic()
                response: Response = self.session.request(method, url, **kwargs)
                elapsed = time.monotonic() - start
                self._log_response(rid, response, elapsed)
                return response
            except (ConnectionError, Timeout) as exc:
                last_error = exc
                if attempt < self.retry_count:
                    wait = self.retry_delay * (2 ** attempt)
                    logger.warning(
                        "[%d] %s %s failed (attempt %d/%d): %s. Retrying in %.1fs…",
                        rid, method, url, attempt + 1, self.retry_count + 1, exc, wait,
                    )
                    time.sleep(wait)
                else:
                    logger.error(
                        "[%d] %s %s failed after %d attempts: %s",
                        rid, method, url, self.retry_count + 1, exc,
                    )

        raise last_error  # type: ignore[misc]
