"""
Base API client for App Store Connect
"""

import requests
from typing import Dict, Any, Optional, List
from urllib.parse import urljoin

from .auth import Auth
from .exceptions import (
    AppStoreConnectError,
    RateLimitError,
    NotFoundError,
    ValidationError,
    ConflictError,
)


class BaseAPI:
    """
    Base class for all API modules
    """
    
    BASE_URL = "https://api.appstoreconnect.apple.com/v1/"
    
    def __init__(self, auth: Auth):
        """
        Initialize base API
        
        Args:
            auth: Authentication instance
        """
        self.auth = auth
        self.session = requests.Session()
        self.session.headers.update(self.auth.headers)
    
    def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict] = None,
        params: Optional[Dict] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Make an API request
        
        Args:
            method: HTTP method
            endpoint: API endpoint
            data: Request body data
            params: Query parameters
            **kwargs: Additional request arguments
            
        Returns:
            JSON response data
            
        Raises:
            Various AppStoreConnectError subclasses
        """
        url = urljoin(self.BASE_URL, endpoint)
        
        # Refresh auth headers
        self.session.headers.update(self.auth.headers)
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                json=data,
                params=params,
                **kwargs
            )
        except requests.RequestException as e:
            raise AppStoreConnectError(f"Request failed: {e}")
        
        # Handle different status codes
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 201:
            return response.json()
        elif response.status_code == 204:
            return {}
        elif response.status_code == 401:
            raise AppStoreConnectError("Authentication failed. Check your credentials.")
        elif response.status_code == 403:
            raise AppStoreConnectError("Forbidden. Check your permissions.")
        elif response.status_code == 404:
            raise NotFoundError(f"Resource not found: {endpoint}")
        elif response.status_code == 409:
            error_msg = self._extract_error_message(response)
            raise ConflictError(error_msg or "Conflict occurred")
        elif response.status_code == 422:
            error_msg = self._extract_error_message(response)
            raise ValidationError(error_msg or "Validation failed")
        elif response.status_code == 429:
            raise RateLimitError("API rate limit exceeded. Please wait before retrying.")
        else:
            error_msg = self._extract_error_message(response)
            raise AppStoreConnectError(
                f"API request failed with status {response.status_code}: {error_msg}"
            )
    
    def _extract_error_message(self, response: requests.Response) -> Optional[str]:
        """Extract error message from response"""
        try:
            data = response.json()
            if 'errors' in data and len(data['errors']) > 0:
                return data['errors'][0].get('title') or data['errors'][0].get('detail')
        except:
            return response.text
        return None
    
    def get(self, endpoint: str, params: Optional[Dict] = None, **kwargs) -> Dict[str, Any]:
        """Make a GET request"""
        return self._request('GET', endpoint, params=params, **kwargs)
    
    def post(self, endpoint: str, data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """Make a POST request"""
        return self._request('POST', endpoint, data=data, **kwargs)
    
    def patch(self, endpoint: str, data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """Make a PATCH request"""
        return self._request('PATCH', endpoint, data=data, **kwargs)
    
    def delete(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make a DELETE request"""
        return self._request('DELETE', endpoint, **kwargs)
    
    def get_all_pages(
        self,
        endpoint: str,
        params: Optional[Dict] = None,
        limit: int = 200
    ) -> List[Dict[str, Any]]:
        """
        Get all pages of results from a paginated endpoint
        
        Args:
            endpoint: API endpoint
            params: Query parameters
            limit: Number of results per page (max 200)
            
        Returns:
            List of all results
        """
        if params is None:
            params = {}
        
        params['limit'] = min(limit, 200)
        all_results = []
        
        while True:
            response = self.get(endpoint, params=params)
            data = response.get('data', [])
            all_results.extend(data)
            
            # Check for next page
            links = response.get('links', {})
            if 'next' not in links:
                break
            
            # Parse next URL for continuation
            # Note: In production, you'd parse the URL properly
            endpoint = links['next'].replace(self.BASE_URL, '')
            params = {}  # Next URL includes params
        
        return all_results