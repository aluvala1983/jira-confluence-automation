"""Utilities for fetching structured report data from HTTP endpoints."""

from __future__ import annotations

from typing import Any, Mapping

import requests


DEFAULT_TIMEOUT = 10


def fetch_json(url: str, *, timeout: int = DEFAULT_TIMEOUT, headers: Mapping[str, str] | None = None, params: Mapping[str, Any] | None = None) -> Any:
    """Fetch JSON from a URL and raise a clear error when the request fails."""
    response = requests.get(url, headers=dict(headers or {}), params=dict(params or {}), timeout=timeout)
    response.raise_for_status()
    try:
        return response.json()
    except ValueError as exc:  # pragma: no cover - defensive branch
        raise ValueError(f"Response from {url!r} was not valid JSON.") from exc
