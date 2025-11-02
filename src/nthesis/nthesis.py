"""HTTP client for interacting with the nthesis API."""

from __future__ import annotations

from typing import List, Optional

import requests

from .models import NewItemResponse, Store

class NthesisError(Exception):
    """Base exception for errors raised by :class:`Client`."""

class UnauthorizedError(NthesisError):
    """Raised when the API responds with HTTP 401 Unauthorized."""

class ConflictError(NthesisError):
    """Raised when the API responds with HTTP 409 Conflict."""

class BadRequestError(NthesisError):
    """Raised when the API responds with HTTP 400 Bad Request."""

class NotFoundError(NthesisError):
    """Raised when the requested resource cannot be found."""

class UnexpectedResponseError(NthesisError):
    """Raised when an unexpected HTTP response is returned by the API."""

    def __init__(self, status_code: int, body: str):
        message = f"unexpected status {status_code}: {body}"
        super().__init__(message)
        self.status_code = status_code
        self.body = body


class Nthesis:
    """Client for nthesis.ai API"""
    def __init__(
        self,
        base_address: str | None = "https://nthesis.ai",
        api_key: str | None = None,
        *,
        session: Optional[requests.Session] = None,
    ) -> None:
        if not base_address:
            raise ValueError("base_address must be provided")

        base = base_address.rstrip("/")
        if not base.endswith("/api/v1"):
            base = f"{base}/api/v1"

        self._base_address = base
        self._api_key = api_key or ""
        self._session = session or requests.Session()

    def list_stores(self, *, timeout: Optional[float] = None) -> List[Store]:
        """Return all stores accessible by the authenticated user."""

        response = self._request("GET", "/stores", timeout=timeout)

        if response.status_code == 200:
            try:
                payload = response.json()
            except ValueError as exc:  # pragma: no cover - malformed JSON
                raise UnexpectedResponseError(response.status_code, response.text) from exc

            stores = payload.get("stores", [])
            if not isinstance(stores, list):
                raise UnexpectedResponseError(response.status_code, response.text)

            return [Store.from_dict(item) for item in stores]

        if response.status_code == 401:
            raise UnauthorizedError("API request is unauthorized")

        raise UnexpectedResponseError(response.status_code, response.text)

    def add_item(
        self,
        store_id: str,
        content: str,
        *,
        timeout: Optional[float] = None,
    ) -> NewItemResponse:
        """Create a new item in the specified store."""

        if not store_id:
            raise ValueError("store_id must be provided")
        if content is None:
            raise ValueError("content must be provided")

        response = self._request(
            "POST",
            "/items",
            json={"content": content},
            params={"storeId": store_id},
            timeout=timeout,
        )

        if response.status_code == 201:
            try:
                payload = response.json()
            except ValueError as exc:  # pragma: no cover - malformed JSON
                raise UnexpectedResponseError(response.status_code, response.text) from exc

            return NewItemResponse.from_dict(payload)

        if response.status_code == 400:
            raise BadRequestError(response.text or "request body is invalid")
        if response.status_code in {401, 403}:
            raise UnauthorizedError("API request is unauthorized")
        if response.status_code == 404:
            raise NotFoundError("store not found")
        if response.status_code == 409:
            raise ConflictError("item already exists")

        raise UnexpectedResponseError(response.status_code, response.text)

    def resolve_store(
        self,
        name: str,
        *,
        email: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> Store:
        """Resolve a store by its name and optional owner email."""

        if not name:
            raise ValueError("name must be provided")

        params = {"name": name}
        if email:
            params["email"] = email

        response = self._request(
            "GET",
            "/stores/resolve",
            params=params,
            timeout=timeout,
        )

        if response.status_code == 200:
            try:
                payload = response.json()
            except ValueError as exc:  # pragma: no cover - malformed JSON
                raise UnexpectedResponseError(response.status_code, response.text) from exc

            return Store.from_dict(payload)

        if response.status_code == 400:
            raise BadRequestError(response.text or "request query parameters are invalid")
        if response.status_code == 401:
            raise UnauthorizedError("API request is unauthorized")
        if response.status_code == 404:
            raise NotFoundError("store not found")

        raise UnexpectedResponseError(response.status_code, response.text)

    def _request(self, method: str, path: str, **kwargs) -> requests.Response:
        url = self._build_url(path)
        headers = kwargs.pop("headers", {})
        if self._api_key:
            headers.setdefault("X-API-Key", self._api_key)

        try:
            response = self._session.request(method, url, headers=headers, **kwargs)
        except requests.RequestException as exc:  # pragma: no cover - network failure
            raise NthesisError(str(exc)) from exc

        return response

    def _build_url(self, path: str) -> str:
        if path.startswith("http://") or path.startswith("https://"):
            return path

        if not path.startswith("/"):
            path = f"/{path}"
        return f"{self._base_address}{path}"


__all__ = [
    "Nthesis",
    "NthesisError",
    "UnauthorizedError",
    "ConflictError",
    "BadRequestError",
    "NotFoundError",
    "UnexpectedResponseError",
]
