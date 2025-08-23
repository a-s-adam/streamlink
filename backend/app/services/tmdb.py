"""TMDB service for metadata enrichment.

This module handles fetching metadata from The Movie Database (TMDB) API.
"""
import logging
import requests
from typing import List, Dict, Any, Optional
from datetime import datetime

from ..config import get_settings

logger = logging.getLogger(__name__)


class TMDBService:
    """Service for interacting with TMDB API."""
    
    def __init__(self):
        settings = get_settings()
        self.api_key = settings.tmdb_api_key
        self.base_url = "https://api.themoviedb.org/3"
        self.mock_mode = getattr(settings, 'mock_mode', False)
        
        if not self.api_key and not self.mock_mode:
            logger.warning("No TMDB API key provided and mock mode disabled")
    
    def search_item(self, title: str, year: Optional[int] = None) -> List[Dict[str, Any]]:
        """Search for an item by title and optionally year."""
        try:
            if self.mock_mode:
                return self._get_mock_results(title, year)
            
            if not self.api_key:
                logger.warning("No TMDB API key available")
                return []
            
            # Build search query
            params = {
                "api_key": self.api_key,
                "query": title,
                "language": "en-US",
                "page": 1,
                "include_adult": False
            }
            
            if year:
                params["year"] = year
            
            # Search in both movies and TV shows
            results = []
            
            # Search movies
            movie_results = self._search_movies(params)
            results.extend(movie_results)
            
            # Search TV shows
            tv_results = self._search_tv_shows(params)
            results.extend(tv_results)
            
            # Sort by relevance (popularity)
            results.sort(key=lambda x: x.get("popularity", 0), reverse=True)
            
            logger.info(f"Found {len(results)} results for '{title}'")
            return results[:10]  # Return top 10 results
            
        except Exception as e:
            logger.error(f"Error searching TMDB for '{title}': {e}")
            return []
    
    def _search_movies(self, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Search for movies."""
        try:
            response = requests.get(
                f"{self.base_url}/search/movie",
                params=params,
                timeout=10
            )
            response.raise_for_status()
            
            data = response.json()
            results = data.get("results", [])
            
            # Add media type
            for result in results:
                result["media_type"] = "movie"
            
            return results
            
        except Exception as e:
            logger.error(f"Error searching movies: {e}")
            return []
    
    def _search_tv_shows(self, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Search for TV shows."""
        try:
            response = requests.get(
                f"{self.base_url}/search/tv",
                params=params,
                timeout=10
            )
            response.raise_for_status()
            
            data = response.json()
            results = data.get("results", [])
            
            # Add media type
            for result in results:
                result["media_type"] = "tv"
            
            return results
            
        except Exception as e:
            logger.error(f"Error searching TV shows: {e}")
            return []
    
    def get_item_details(self, tmdb_id: str, media_type: str) -> Optional[Dict[str, Any]]:
        """Get detailed information for a specific item."""
        try:
            if self.mock_mode:
                return self._get_mock_details(tmdb_id, media_type)
            
            if not self.api_key:
                logger.warning("No TMDB API key available")
                return None
            
            params = {
                "api_key": self.api_key,
                "language": "en-US",
                "append_to_response": "credits,genres"
            }
            
            response = requests.get(
                f"{self.base_url}/{media_type}/{tmdb_id}",
                params=params,
                timeout=10
            )
            response.raise_for_status()
            
            data = response.json()
            
            # Add media type
            data["media_type"] = media_type
            
            logger.info(f"Retrieved details for {media_type} {tmdb_id}")
            return data
            
        except Exception as e:
            logger.error(f"Error getting details for {media_type} {tmdb_id}: {e}")
            return None
    
    def _get_mock_results(self, title: str, year: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get mock search results for testing."""
        mock_results = [
            {
                "id": 12345,
                "title": title,
                "name": title,  # TV shows use 'name'
                "overview": f"A mock overview for {title}",
                "poster_path": "/mock-poster.jpg",
                "popularity": 8.5,
                "media_type": "movie",
                "release_date": f"{year or 2024}-01-01" if year else "2024-01-01",
                "genres": [{"id": 1, "name": "Drama"}, {"id": 2, "name": "Thriller"}],
                "runtime": 120
            }
        ]
        
        logger.info(f"Returning mock results for '{title}'")
        return mock_results
    
    def _get_mock_details(self, tmdb_id: str, media_type: str) -> Dict[str, Any]:
        """Get mock details for testing."""
        mock_details = {
            "id": tmdb_id,
            "title": f"Mock {media_type.title()}",
            "name": f"Mock {media_type.title()}",  # TV shows use 'name'
            "overview": f"A mock overview for {media_type} {tmdb_id}",
            "poster_path": "/mock-poster.jpg",
            "backdrop_path": "/mock-backdrop.jpg",
            "popularity": 8.5,
            "media_type": media_type,
            "release_date": "2024-01-01",
            "first_air_date": "2024-01-01",  # TV shows
            "genres": [{"id": 1, "name": "Drama"}, {"id": 2, "name": "Thriller"}],
            "runtime": 120,
            "episode_run_time": [45],  # TV shows
            "number_of_seasons": 1,
            "number_of_episodes": 10
        }
        
        logger.info(f"Returning mock details for {media_type} {tmdb_id}")
        return mock_details
