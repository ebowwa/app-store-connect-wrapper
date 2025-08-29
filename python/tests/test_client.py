"""
Tests for main client
"""

import unittest
from unittest.mock import patch, MagicMock, Mock
from pathlib import Path
import os

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from app_store_connect.client import Client
from app_store_connect.auth import Auth


class TestClient(unittest.TestCase):
    """Test cases for Client class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.key_id = "TEST_KEY_ID"
        self.issuer_id = "TEST_ISSUER_ID"
        self.private_key_path = "/path/to/test.p8"
    
    @patch('app_store_connect.auth.Path.exists', return_value=True)
    @patch('builtins.open')
    def test_init_with_credentials(self, mock_open, mock_exists):
        """Test client initialization with credentials"""
        mock_open.return_value.__enter__.return_value.read.return_value = "mock_key"
        
        client = Client(
            key_id=self.key_id,
            issuer_id=self.issuer_id,
            private_key_path=self.private_key_path
        )
        
        self.assertIsNotNone(client.apps)
        self.assertIsNotNone(client.localizations)
        self.assertIsNotNone(client.version_localizations)
        self.assertIsNotNone(client.versions)
    
    @patch('app_store_connect.auth.Path.exists', return_value=True)
    @patch('builtins.open')
    def test_init_with_auth_object(self, mock_open, mock_exists):
        """Test client initialization with Auth object"""
        mock_open.return_value.__enter__.return_value.read.return_value = "mock_key"
        
        auth = Auth(self.key_id, self.issuer_id, self.private_key_path)
        client = Client(
            key_id="ignored",
            issuer_id="ignored",
            private_key_path="ignored",
            auth=auth
        )
        
        self.assertEqual(client._auth, auth)
    
    @patch.dict(os.environ, {
        'ASC_KEY_ID': 'ENV_KEY_ID',
        'ASC_ISSUER_ID': 'ENV_ISSUER_ID',
        'ASC_PRIVATE_KEY_PATH': '/env/path/key.p8'
    })
    @patch('app_store_connect.auth.Path.exists', return_value=True)
    @patch('builtins.open')
    def test_from_env(self, mock_open, mock_exists):
        """Test client creation from environment variables"""
        mock_open.return_value.__enter__.return_value.read.return_value = "mock_key"
        
        client = Client.from_env()
        
        self.assertIsNotNone(client)
        self.assertEqual(client._auth.key_id, 'ENV_KEY_ID')
        self.assertEqual(client._auth.issuer_id, 'ENV_ISSUER_ID')
    
    @patch.dict(os.environ, {})
    def test_from_env_missing_vars(self):
        """Test from_env with missing environment variables"""
        with self.assertRaises(ValueError) as context:
            Client.from_env()
        
        self.assertIn("Missing required environment variables", str(context.exception))
    
    @patch('app_store_connect.auth.Path.exists', return_value=True)
    @patch('builtins.open')
    def test_get_app_by_bundle_id(self, mock_open, mock_exists):
        """Test getting app by bundle ID"""
        mock_open.return_value.__enter__.return_value.read.return_value = "mock_key"
        
        client = Client(
            key_id=self.key_id,
            issuer_id=self.issuer_id,
            private_key_path=self.private_key_path
        )
        
        # Mock the apps API
        client.apps.get_by_bundle_id = MagicMock(return_value={'id': 'app123'})
        
        result = client.get_app_by_bundle_id('com.example.app')
        
        self.assertEqual(result, {'id': 'app123'})
        client.apps.get_by_bundle_id.assert_called_once_with('com.example.app')
    
    @patch('app_store_connect.auth.Path.exists', return_value=True)
    @patch('builtins.open')
    def test_update_app_localizations(self, mock_open, mock_exists):
        """Test updating app localizations"""
        mock_open.return_value.__enter__.return_value.read.return_value = "mock_key"
        
        client = Client(
            key_id=self.key_id,
            issuer_id=self.issuer_id,
            private_key_path=self.private_key_path
        )
        
        # Mock the APIs
        client.apps.get_app_infos = MagicMock(return_value=[{'id': 'info123'}])
        client.localizations.bulk_update = MagicMock(return_value={
            'en-US': {'success': True}
        })
        
        localizations = {'en-US': {'name': 'Test App'}}
        result = client.update_app_localizations('app123', localizations)
        
        self.assertEqual(result, {'en-US': {'success': True}})
        client.apps.get_app_infos.assert_called_once_with('app123')
        client.localizations.bulk_update.assert_called_once_with('info123', localizations)
    
    @patch('app_store_connect.auth.Path.exists', return_value=True)
    @patch('builtins.open')
    def test_update_app_localizations_no_info(self, mock_open, mock_exists):
        """Test updating app localizations with no app info"""
        mock_open.return_value.__enter__.return_value.read.return_value = "mock_key"
        
        client = Client(
            key_id=self.key_id,
            issuer_id=self.issuer_id,
            private_key_path=self.private_key_path
        )
        
        # Mock empty app infos
        client.apps.get_app_infos = MagicMock(return_value=[])
        
        with self.assertRaises(ValueError) as context:
            client.update_app_localizations('app123', {})
        
        self.assertIn("No app info found", str(context.exception))
    
    @patch('app_store_connect.auth.Path.exists', return_value=True)
    @patch('builtins.open')
    def test_get_current_version(self, mock_open, mock_exists):
        """Test getting current version"""
        mock_open.return_value.__enter__.return_value.read.return_value = "mock_key"
        
        client = Client(
            key_id=self.key_id,
            issuer_id=self.issuer_id,
            private_key_path=self.private_key_path
        )
        
        client.versions.get_current = MagicMock(return_value={'version': '1.0.0'})
        
        result = client.get_current_version('app123')
        
        self.assertEqual(result, {'version': '1.0.0'})
        client.versions.get_current.assert_called_once_with('app123')
    
    @patch('app_store_connect.auth.Path.exists', return_value=True)
    @patch('builtins.open')
    def test_create_new_version(self, mock_open, mock_exists):
        """Test creating new version"""
        mock_open.return_value.__enter__.return_value.read.return_value = "mock_key"
        
        client = Client(
            key_id=self.key_id,
            issuer_id=self.issuer_id,
            private_key_path=self.private_key_path
        )
        
        client.versions.create = MagicMock(return_value={'id': 'v123'})
        
        result = client.create_new_version('app123', '1.0.1', platform='IOS')
        
        self.assertEqual(result, {'id': 'v123'})
        client.versions.create.assert_called_once_with('app123', '1.0.1', platform='IOS')
    
    @patch('app_store_connect.auth.Path.exists', return_value=True)
    @patch('builtins.open')
    def test_submit_for_review(self, mock_open, mock_exists):
        """Test submitting for review"""
        mock_open.return_value.__enter__.return_value.read.return_value = "mock_key"
        
        client = Client(
            key_id=self.key_id,
            issuer_id=self.issuer_id,
            private_key_path=self.private_key_path
        )
        
        client.versions.submit_for_review = MagicMock(return_value={'status': 'submitted'})
        
        result = client.submit_for_review('v123')
        
        self.assertEqual(result, {'status': 'submitted'})
        client.versions.submit_for_review.assert_called_once_with('v123')


if __name__ == '__main__':
    unittest.main()
