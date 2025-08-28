"""
Tests for base API class
"""

import unittest
from unittest.mock import patch, MagicMock, Mock
import requests
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from app_store_connect.base import BaseAPI
from app_store_connect.auth import Auth
from app_store_connect.exceptions import (
    AppStoreConnectError,
    RateLimitError,
    NotFoundError,
    ValidationError,
    ConflictError
)


class TestBaseAPI(unittest.TestCase):
    """Test cases for BaseAPI class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.mock_auth = MagicMock(spec=Auth)
        self.mock_auth.headers = {
            'Authorization': 'Bearer test_token',
            'Content-Type': 'application/json'
        }
        self.base_api = BaseAPI(self.mock_auth)
    
    def test_init(self):
        """Test BaseAPI initialization"""
        self.assertEqual(self.base_api.auth, self.mock_auth)
        self.assertIsNotNone(self.base_api.session)
        self.assertEqual(
            self.base_api.session.headers['Authorization'],
            'Bearer test_token'
        )
    
    @patch('app_store_connect.base.requests.Session')
    def test_request_success_200(self, mock_session_class):
        """Test successful request with 200 status"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'data': 'test'}
        
        mock_session = MagicMock()
        mock_session.request.return_value = mock_response
        mock_session_class.return_value = mock_session
        
        api = BaseAPI(self.mock_auth)
        result = api._request('GET', 'test/endpoint')
        
        self.assertEqual(result, {'data': 'test'})
    
    @patch('app_store_connect.base.requests.Session')
    def test_request_success_201(self, mock_session_class):
        """Test successful request with 201 status"""
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.json.return_value = {'created': True}
        
        mock_session = MagicMock()
        mock_session.request.return_value = mock_response
        mock_session_class.return_value = mock_session
        
        api = BaseAPI(self.mock_auth)
        result = api._request('POST', 'test/endpoint')
        
        self.assertEqual(result, {'created': True})
    
    @patch('app_store_connect.base.requests.Session')
    def test_request_success_204(self, mock_session_class):
        """Test successful request with 204 status (no content)"""
        mock_response = MagicMock()
        mock_response.status_code = 204
        
        mock_session = MagicMock()
        mock_session.request.return_value = mock_response
        mock_session_class.return_value = mock_session
        
        api = BaseAPI(self.mock_auth)
        result = api._request('DELETE', 'test/endpoint')
        
        self.assertEqual(result, {})
    
    @patch('app_store_connect.base.requests.Session')
    def test_request_auth_error(self, mock_session_class):
        """Test authentication error (401)"""
        mock_response = MagicMock()
        mock_response.status_code = 401
        
        mock_session = MagicMock()
        mock_session.request.return_value = mock_response
        mock_session_class.return_value = mock_session
        
        api = BaseAPI(self.mock_auth)
        
        with self.assertRaises(AppStoreConnectError) as context:
            api._request('GET', 'test/endpoint')
        
        self.assertIn("Authentication failed", str(context.exception))
    
    @patch('app_store_connect.base.requests.Session')
    def test_request_forbidden(self, mock_session_class):
        """Test forbidden error (403)"""
        mock_response = MagicMock()
        mock_response.status_code = 403
        
        mock_session = MagicMock()
        mock_session.request.return_value = mock_response
        mock_session_class.return_value = mock_session
        
        api = BaseAPI(self.mock_auth)
        
        with self.assertRaises(AppStoreConnectError) as context:
            api._request('GET', 'test/endpoint')
        
        self.assertIn("Forbidden", str(context.exception))
    
    @patch('app_store_connect.base.requests.Session')
    def test_request_not_found(self, mock_session_class):
        """Test not found error (404)"""
        mock_response = MagicMock()
        mock_response.status_code = 404
        
        mock_session = MagicMock()
        mock_session.request.return_value = mock_response
        mock_session_class.return_value = mock_session
        
        api = BaseAPI(self.mock_auth)
        
        with self.assertRaises(NotFoundError) as context:
            api._request('GET', 'test/endpoint')
        
        self.assertIn("Resource not found", str(context.exception))
    
    @patch('app_store_connect.base.requests.Session')
    def test_request_conflict(self, mock_session_class):
        """Test conflict error (409)"""
        mock_response = MagicMock()
        mock_response.status_code = 409
        mock_response.json.return_value = {
            'errors': [{'title': 'Name already exists'}]
        }
        
        mock_session = MagicMock()
        mock_session.request.return_value = mock_response
        mock_session_class.return_value = mock_session
        
        api = BaseAPI(self.mock_auth)
        
        with self.assertRaises(ConflictError) as context:
            api._request('POST', 'test/endpoint')
        
        self.assertIn("Name already exists", str(context.exception))
    
    @patch('app_store_connect.base.requests.Session')
    def test_request_validation_error(self, mock_session_class):
        """Test validation error (422)"""
        mock_response = MagicMock()
        mock_response.status_code = 422
        mock_response.json.return_value = {
            'errors': [{'detail': 'Invalid field value'}]
        }
        
        mock_session = MagicMock()
        mock_session.request.return_value = mock_response
        mock_session_class.return_value = mock_session
        
        api = BaseAPI(self.mock_auth)
        
        with self.assertRaises(ValidationError) as context:
            api._request('POST', 'test/endpoint')
        
        self.assertIn("Invalid field value", str(context.exception))
    
    @patch('app_store_connect.base.requests.Session')
    def test_request_rate_limit(self, mock_session_class):
        """Test rate limit error (429)"""
        mock_response = MagicMock()
        mock_response.status_code = 429
        
        mock_session = MagicMock()
        mock_session.request.return_value = mock_response
        mock_session_class.return_value = mock_session
        
        api = BaseAPI(self.mock_auth)
        
        with self.assertRaises(RateLimitError) as context:
            api._request('GET', 'test/endpoint')
        
        self.assertIn("API rate limit exceeded", str(context.exception))
    
    @patch('app_store_connect.base.requests.Session')
    def test_get_all_pages(self, mock_session_class):
        """Test pagination handling"""
        # First page response
        first_response = MagicMock()
        first_response.status_code = 200
        first_response.json.return_value = {
            'data': [{'id': '1'}, {'id': '2'}],
            'links': {'next': 'https://api.appstoreconnect.apple.com/v1/next_page'}
        }
        
        # Second page response
        second_response = MagicMock()
        second_response.status_code = 200
        second_response.json.return_value = {
            'data': [{'id': '3'}],
            'links': {}  # No next page
        }
        
        mock_session = MagicMock()
        mock_session.request.side_effect = [first_response, second_response]
        mock_session_class.return_value = mock_session
        
        api = BaseAPI(self.mock_auth)
        result = api.get_all_pages('test/endpoint')
        
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0]['id'], '1')
        self.assertEqual(result[2]['id'], '3')
    
    def test_get_method(self):
        """Test GET method wrapper"""
        with patch.object(self.base_api, '_request') as mock_request:
            mock_request.return_value = {'success': True}
            
            result = self.base_api.get('test/endpoint', params={'filter': 'test'})
            
            mock_request.assert_called_once_with(
                'GET',
                'test/endpoint',
                params={'filter': 'test'}
            )
            self.assertEqual(result, {'success': True})
    
    def test_post_method(self):
        """Test POST method wrapper"""
        with patch.object(self.base_api, '_request') as mock_request:
            mock_request.return_value = {'created': True}
            
            data = {'name': 'Test'}
            result = self.base_api.post('test/endpoint', data)
            
            mock_request.assert_called_once_with(
                'POST',
                'test/endpoint',
                data=data
            )
            self.assertEqual(result, {'created': True})
    
    def test_patch_method(self):
        """Test PATCH method wrapper"""
        with patch.object(self.base_api, '_request') as mock_request:
            mock_request.return_value = {'updated': True}
            
            data = {'name': 'Updated'}
            result = self.base_api.patch('test/endpoint', data)
            
            mock_request.assert_called_once_with(
                'PATCH',
                'test/endpoint',
                data=data
            )
            self.assertEqual(result, {'updated': True})
    
    def test_delete_method(self):
        """Test DELETE method wrapper"""
        with patch.object(self.base_api, '_request') as mock_request:
            mock_request.return_value = {}
            
            result = self.base_api.delete('test/endpoint')
            
            mock_request.assert_called_once_with(
                'DELETE',
                'test/endpoint'
            )
            self.assertEqual(result, {})


if __name__ == '__main__':
    unittest.main()