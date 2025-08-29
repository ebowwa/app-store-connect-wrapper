"""
Tests for authentication module
"""

import unittest
from unittest.mock import patch, mock_open, MagicMock
import time
import jwt
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from app_store_connect.auth import Auth
from app_store_connect.exceptions import AuthenticationError


class TestAuth(unittest.TestCase):
    """Test cases for Auth class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.key_id = "TEST_KEY_ID"
        self.issuer_id = "TEST_ISSUER_ID"
        self.private_key_path = "/path/to/test.p8"
        self.mock_private_key = """-----BEGIN PRIVATE KEY-----
MIGTAgEAMBMGByqGSM49AgEGCCqGSM49AwEHBHkwdwIBAQQg/HUW5uT+WxOqLhF7
Uo6kQmJET3hjGSZT3J8HvRbFbY+gCgYIKoZIzj0DAQehRANCAAQPscnMvEzfvZPg
4OGJwX3+ulMLULHqFhgnPjvFUdHa9EqJuVdzwgUSmcJlDvpe+RfLINYlg5gKvbK2
vz1m9tKI
-----END PRIVATE KEY-----"""
    
    @patch('app_store_connect.auth.Path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_init_success(self, mock_file, mock_exists):
        """Test successful initialization"""
        mock_exists.return_value = True
        mock_file.return_value.read.return_value = self.mock_private_key
        
        auth = Auth(self.key_id, self.issuer_id, self.private_key_path)
        
        self.assertEqual(auth.key_id, self.key_id)
        self.assertEqual(auth.issuer_id, self.issuer_id)
        self.assertEqual(auth.private_key_path, Path(self.private_key_path))
        self.assertEqual(auth.private_key, self.mock_private_key)
    
    @patch('app_store_connect.auth.Path.exists')
    def test_init_file_not_found(self, mock_exists):
        """Test initialization with missing private key file"""
        mock_exists.return_value = False
        
        with self.assertRaises(AuthenticationError) as context:
            Auth(self.key_id, self.issuer_id, self.private_key_path)
        
        self.assertIn("Private key file not found", str(context.exception))
    
    @patch('app_store_connect.auth.Path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_generate_token(self, mock_file, mock_exists):
        """Test JWT token generation"""
        mock_exists.return_value = True
        mock_file.return_value.read.return_value = self.mock_private_key
        
        auth = Auth(self.key_id, self.issuer_id, self.private_key_path)
        
        # Mock time to control token generation
        with patch('time.time', return_value=1000):
            auth._generate_token()
        
        self.assertIsNotNone(auth._token)
        self.assertEqual(auth._token_expiry, 1000 + (20 * 60))
    
    @patch('app_store_connect.auth.Path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_get_token_refresh(self, mock_file, mock_exists):
        """Test token refresh when expired"""
        mock_exists.return_value = True
        mock_file.return_value.read.return_value = self.mock_private_key
        
        auth = Auth(self.key_id, self.issuer_id, self.private_key_path)
        
        # Set expired token
        auth._token = "old_token"
        auth._token_expiry = time.time() - 100  # Expired
        
        # Get new token
        new_token = auth.get_token()
        
        self.assertNotEqual(new_token, "old_token")
        self.assertIsNotNone(new_token)
    
    @patch('app_store_connect.auth.Path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_get_token_reuse(self, mock_file, mock_exists):
        """Test token reuse when still valid"""
        mock_exists.return_value = True
        mock_file.return_value.read.return_value = self.mock_private_key
        
        auth = Auth(self.key_id, self.issuer_id, self.private_key_path)
        
        # Generate initial token
        auth._generate_token()
        first_token = auth._token
        
        # Set expiry in future
        auth._token_expiry = time.time() + 1000
        
        # Get token again
        second_token = auth.get_token()
        
        self.assertEqual(first_token, second_token)
    
    @patch('app_store_connect.auth.Path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_headers(self, mock_file, mock_exists):
        """Test headers property"""
        mock_exists.return_value = True
        mock_file.return_value.read.return_value = self.mock_private_key
        
        auth = Auth(self.key_id, self.issuer_id, self.private_key_path)
        headers = auth.headers
        
        self.assertIn('Authorization', headers)
        self.assertIn('Bearer ', headers['Authorization'])
        self.assertEqual(headers['Content-Type'], 'application/json')
    
    @patch('app_store_connect.auth.Path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_is_token_valid(self, mock_file, mock_exists):
        """Test token validity check"""
        mock_exists.return_value = True
        mock_file.return_value.read.return_value = self.mock_private_key
        
        auth = Auth(self.key_id, self.issuer_id, self.private_key_path)
        
        # No token yet
        self.assertFalse(auth.is_token_valid())
        
        # Generate token
        auth._generate_token()
        self.assertTrue(auth.is_token_valid())
        
        # Expire token
        auth._token_expiry = time.time() - 100
        self.assertFalse(auth.is_token_valid())


if __name__ == '__main__':
    unittest.main()
