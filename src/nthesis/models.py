"""Data models for the nthesis Python client."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict


@dataclass(frozen=True)
class Store:
    """Represents a store resource exposed by the nthesis API."""

    id: str
    name: str
    owner_email: str
    permissions: str
    is_owned: bool
    is_global: bool

    @classmethod
    def from_dict(cls, payload: Dict[str, Any]) -> "Store":
        """Create a :class:`Store` from an API response dictionary."""

        if not isinstance(payload, dict):
            raise TypeError("payload must be a dictionary")

        return cls(
            id=str(payload.get("id", "")),
            name=str(payload.get("name", "")),
            owner_email=str(payload.get("ownerEmail", "")),
            permissions=str(payload.get("permissions", "")),
            is_owned=bool(payload.get("isOwned", False)),
            is_global=bool(payload.get("isGlobal", False)),
        )


@dataclass(frozen=True)
class NewItemResponse:
    """Represents the response when creating a new item."""

    id: str
    store_id: str
    hash: str

    @classmethod
    def from_dict(cls, payload: Dict[str, Any]) -> "NewItemResponse":
        if not isinstance(payload, dict):
            raise TypeError("payload must be a dictionary")

        return cls(
            id=str(payload.get("id", "")),
            store_id=str(payload.get("storeId", "")),
            hash=str(payload.get("hash", "")),
        )
