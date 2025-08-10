"""TMDB API client.

This module provides a minimal wrapper around the TMDB (The Movie Database)
API to fetch metadata for movies and TV shows.  In a full implementation
you would handle rate limiting, caching, and error handling gracefully.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, Optional

import requests

from ..config import get_settings

logger = logging.getLogger(__name__)


def search_title(title: str) -> Optional[Dict[str, Any]]:
    """Search TMDB for a title and return the first result.

    Returns a dictionary containing metadata such as TMDB ID, overview,
    release date, and popularity.  If no result is found or the API key is
    missing, ``None`` is returned.
    """
    settings = get_settings()
    api_key = settings.tmdb_api_key
    if not api_key:
        logger.warning("TMDB_API_KEY is not configured; metadata lookups are disabled")
        return None
    try:
        response = requests.get(
            "https://api.themoviedb.org/3/search/multi",
            params={"api_key": api_key, "query": title, "include_adult": "false"},
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()
        results = data.get("results") or []
        if not results:
            return None
        # Return the first result
        return results[0]
    except Exception as exc:
        logger.error("TMDB lookup failed for '%s': %s", title, exc)
        return None
