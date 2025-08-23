"""YouTube service for OAuth and data fetching.

This module handles YouTube OAuth flow and fetching viewing history.
"""
import logging
import json
from typing import List, Dict, Any, Optional
from datetime import datetime

from ..config import get_settings

logger = logging.getLogger(__name__)


class YouTubeService:
    """Service for interacting with YouTube Data API."""
    
    def __init__(self):
        settings = get_settings()
        self.api_key = settings.youtube_api_key
        self.client_id = settings.youtube_oauth_client_id
        self.client_secret = settings.youtube_oauth_client_secret
        self.redirect_uri = settings.youtube_redirect_uri
        self.mock_mode = getattr(settings, 'mock_mode', False)
        
        if not self.api_key and not self.mock_mode:
            logger.warning("No YouTube API key provided and mock mode disabled")
    
    def get_oauth_url(self) -> str:
        """Generate OAuth URL for YouTube authorization."""
        if self.mock_mode:
            return "http://localhost:3000/mock-youtube-auth"
        
        if not self.client_id:
            raise ValueError("YouTube OAuth client ID not configured")
        
        # YouTube OAuth 2.0 URL
        oauth_url = (
            "https://accounts.google.com/o/oauth2/v2/auth?"
            f"client_id={self.client_id}&"
            "response_type=code&"
            "scope=https://www.googleapis.com/auth/youtube.readonly&"
            f"redirect_uri={self.redirect_uri}&"
            "access_type=offline&"
            "prompt=consent"
        )
        
        return oauth_url
    
    def exchange_code_for_tokens(self, auth_code: str) -> Dict[str, Any]:
        """Exchange authorization code for access and refresh tokens."""
        if self.mock_mode:
            return self._get_mock_tokens()
        
        if not self.client_secret:
            raise ValueError("YouTube OAuth client secret not configured")
        
        try:
            import requests
            
            token_url = "https://oauth2.googleapis.com/token"
            data = {
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "code": auth_code,
                "grant_type": "authorization_code",
                "redirect_uri": self.redirect_uri
            }
            
            response = requests.post(token_url, data=data, timeout=10)
            response.raise_for_status()
            
            tokens = response.json()
            logger.info("Successfully exchanged auth code for tokens")
            return tokens
            
        except Exception as e:
            logger.error(f"Error exchanging auth code for tokens: {e}")
            raise
    
    def get_viewing_history(self, access_token: str) -> List[Dict[str, Any]]:
        """Fetch user's YouTube viewing history."""
        if self.mock_mode:
            return self._get_mock_history()
        
        if not self.api_key:
            logger.warning("No YouTube API key available")
            return []
        
        try:
            import requests
            
            # YouTube Data API v3 endpoint for search history
            # Note: YouTube doesn't provide direct access to viewing history via API
            # This is a limitation - we'd need to use the Takeout data or browser extension
            
            # For now, return empty list with warning
            logger.warning("YouTube viewing history not available via API - use Takeout data")
            return []
            
        except Exception as e:
            logger.error(f"Error fetching YouTube history: {e}")
            return []
    
    def get_user_info(self, access_token: str) -> Optional[Dict[str, Any]]:
        """Get basic user information."""
        if self.mock_mode:
            return self._get_mock_user_info()
        
        try:
            import requests
            
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.get(
                "https://www.googleapis.com/oauth2/v2/userinfo",
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            
            user_info = response.json()
            logger.info("Successfully retrieved YouTube user info")
            return user_info
            
        except Exception as e:
            logger.error(f"Error fetching YouTube user info: {e}")
            return None
    
    def _get_mock_tokens(self) -> Dict[str, Any]:
        """Get mock OAuth tokens for testing."""
        return {
            "access_token": "mock_access_token",
            "refresh_token": "mock_refresh_token",
            "expires_in": 3600,
            "token_type": "Bearer"
        }
    
    def _get_mock_history(self) -> List[Dict[str, Any]]:
        """Get mock viewing history for testing."""
        return [
            {
                "header": "YouTube Data",
                "title": "Watched \"Mock YouTube Video 1\"",
                "titleUrl": "https://www.youtube.com/watch?v=mock1",
                "time": "2024-01-15T20:30:00Z",
                "products": ["YouTube"],
                "activityControls": ["YouTube watch history"]
            },
            {
                "header": "YouTube Data",
                "title": "Watched \"Mock YouTube Video 2\"",
                "titleUrl": "https://www.youtube.com/watch?v=mock2",
                "time": "2024-01-15T19:30:00Z",
                "products": ["YouTube"],
                "activityControls": ["YouTube watch history"]
            }
        ]
    
    def _get_mock_user_info(self) -> Dict[str, Any]:
        """Get mock user info for testing."""
        return {
            "id": "mock_user_id",
            "email": "mock@example.com",
            "name": "Mock User",
            "picture": "https://example.com/mock-avatar.jpg"
        }
