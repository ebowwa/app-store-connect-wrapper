"""
Authentication module for App Store Connect API
"""

import jwt
import time
from pathlib import Path
from typing import Optional
from datetime import datetime, timedelta

from .exceptions import AuthenticationError


class Auth:
    """
    Handles JWT authentication for App Store Connect API
    """
    
    def __init__(self, key_id: str, issuer_id: str, private_key_path: str):
        """
        Initialize authentication
        
        Args:
            key_id: Your App Store Connect API Key ID
            issuer_id: Your App Store Connect Issuer ID
            private_key_path: Path to your .p8 private key file
        """
        self.key_id = key_id
        self.issuer_id = issuer_id
        self.private_key_path = Path(private_key_path)
        self._token = None
        self._token_expiry = 0
        
        if not self.private_key_path.exists():
            raise AuthenticationError(f"Private key file not found: {private_key_path}")
        
        self._load_private_key()
    
    def _load_private_key(self):
        """Load the private key from file"""
        try:
            with open(self.private_key_path, 'r') as f:
                self.private_key = f.read()
        except Exception as e:
            raise AuthenticationError(f"Failed to load private key: {e}")
    
    def get_token(self) -> str:
        """
        Get a valid JWT token, refreshing if necessary
        
        Returns:
            JWT token string
        """
        # Check if token is still valid (with 1 minute buffer)
        if self._token and time.time() < (self._token_expiry - 60):
            return self._token
        
        # Generate new token
        self._generate_token()
        return self._token
    
    def _generate_token(self):
        """Generate a new JWT token"""
        # Token expires in 20 minutes (maximum allowed by Apple)
        expiry_time = int(time.time()) + (20 * 60)
        
        payload = {
            'iss': self.issuer_id,
            'iat': int(time.time()),
            'exp': expiry_time,
            'aud': 'appstoreconnect-v1'
        }
        
        headers = {
            'kid': self.key_id,
            'alg': 'ES256',
            'typ': 'JWT'
        }
        
        try:
            self._token = jwt.encode(
                payload,
                self.private_key,
                algorithm='ES256',
                headers=headers
            )
            self._token_expiry = expiry_time
        except Exception as e:
            raise AuthenticationError(f"Failed to generate JWT token: {e}")
    
    @property
    def headers(self) -> dict:
        """
        Get authorization headers for API requests
        
        Returns:
            Dictionary with Authorization header
        """
        return {
            'Authorization': f'Bearer {self.get_token()}',
            'Content-Type': 'application/json'
        }
    
    def is_token_valid(self) -> bool:
        """Check if current token is still valid"""
        return self._token is not None and time.time() < self._token_expiry
    
    def refresh_token(self):
        """Force refresh of the JWT token"""
        self._generate_token()