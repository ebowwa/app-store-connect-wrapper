"""
Integration tests for App Store Connect API wrapper
"""

import unittest
import os
from pathlib import Path
from unittest.mock import patch, MagicMock
from dotenv import load_dotenv

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from app_store_connect import Client
from app_store_connect.exceptions import AppStoreConnectError


class TestIntegration(unittest.TestCase):
    """Integration tests - can be run against real API with valid credentials"""
    
    @classmethod
    def setUpClass(cls):
        """Load environment variables for integration tests"""
        env_path = Path(__file__).parent.parent / '.env'
        if env_path.exists():
            load_dotenv(env_path)
        
        cls.has_credentials = all([
            os.getenv('ASC_KEY_ID'),
            os.getenv('ASC_ISSUER_ID'),
            os.getenv('ASC_PRIVATE_KEY_PATH')
        ])
        
        if cls.has_credentials:
            # Check if private key file exists
            key_path = Path(os.getenv('ASC_PRIVATE_KEY_PATH'))
            cls.has_credentials = key_path.exists()
    
    def setUp(self):
        """Set up test client if credentials are available"""
        if not self.has_credentials:
            self.skipTest("No App Store Connect credentials available")
        
        try:
            self.client = Client.from_env()
            self.app_id = os.getenv('ASC_APP_ID')
        except Exception as e:
            self.skipTest(f"Failed to create client: {e}")
    
    def test_get_all_apps(self):
        """Test getting all apps"""
        try:
            apps = self.client.apps.get_all()
            self.assertIsInstance(apps, list)
            
            if apps:
                # Check structure of first app
                app = apps[0]
                self.assertIn('id', app)
                self.assertIn('attributes', app)
                self.assertIn('name', app['attributes'])
                self.assertIn('bundleId', app['attributes'])
        except AppStoreConnectError as e:
            self.skipTest(f"API error: {e}")
    
    def test_get_app_by_id(self):
        """Test getting specific app"""
        if not self.app_id:
            self.skipTest("No app ID configured")
        
        try:
            app = self.client.apps.get(self.app_id)
            self.assertIsNotNone(app)
            self.assertEqual(app['id'], self.app_id)
        except AppStoreConnectError as e:
            self.skipTest(f"API error: {e}")
    
    def test_get_app_infos(self):
        """Test getting app infos"""
        if not self.app_id:
            self.skipTest("No app ID configured")
        
        try:
            app_infos = self.client.apps.get_app_infos(self.app_id)
            self.assertIsInstance(app_infos, list)
            
            if app_infos:
                info = app_infos[0]
                self.assertIn('id', info)
                self.assertIn('attributes', info)
        except AppStoreConnectError as e:
            self.skipTest(f"API error: {e}")
    
    def test_get_localizations(self):
        """Test getting localizations"""
        if not self.app_id:
            self.skipTest("No app ID configured")
        
        try:
            # Get app infos first
            app_infos = self.client.apps.get_app_infos(self.app_id)
            if not app_infos:
                self.skipTest("No app infos available")
            
            app_info_id = app_infos[0]['id']
            
            # Get localizations
            localizations = self.client.localizations.get_all(app_info_id)
            self.assertIsInstance(localizations, list)
            
            if localizations:
                loc = localizations[0]
                self.assertIn('id', loc)
                self.assertIn('attributes', loc)
                self.assertIn('locale', loc['attributes'])
        except AppStoreConnectError as e:
            self.skipTest(f"API error: {e}")
    
    def test_get_app_store_versions(self):
        """Test getting app store versions"""
        if not self.app_id:
            self.skipTest("No app ID configured")
        
        try:
            versions = self.client.versions.get_all(self.app_id)
            self.assertIsInstance(versions, list)
            
            if versions:
                version = versions[0]
                self.assertIn('id', version)
                self.assertIn('attributes', version)
                self.assertIn('versionString', version['attributes'])
                self.assertIn('appStoreState', version['attributes'])
        except AppStoreConnectError as e:
            self.skipTest(f"API error: {e}")
    
    def test_get_current_version(self):
        """Test getting current version"""
        if not self.app_id:
            self.skipTest("No app ID configured")
        
        try:
            current = self.client.get_current_version(self.app_id)
            # May be None if no versions exist
            if current:
                self.assertIn('id', current)
                self.assertIn('attributes', current)
        except AppStoreConnectError as e:
            self.skipTest(f"API error: {e}")


class TestMockedIntegration(unittest.TestCase):
    """Mocked integration tests that don't require real API access"""
    
    @patch('app_store_connect.auth.Path.exists', return_value=True)
    @patch('builtins.open')
    @patch('app_store_connect.base.requests.Session')
    def test_full_localization_workflow(self, mock_session_class, mock_open, mock_exists):
        """Test complete localization update workflow"""
        # Setup mock private key
        mock_open.return_value.__enter__.return_value.read.return_value = """-----BEGIN PRIVATE KEY-----
MIGTAgEAMBMGByqGSM49AgEGCCqGSM49AwEHBHkwdwIBAQQg/HUW5uT+WxOqLhF7
Uo6kQmJET3hjGSZT3J8HvRbFbY+gCgYIKoZIzj0DAQehRANCAAQPscnMvEzfvZPg
4OGJwX3+ulMLULHqFhgnPjvFUdHa9EqJuVdzwgUSmcJlDvpe+RfLINYlg5gKvbK2
vz1m9tKI
-----END PRIVATE KEY-----"""
        
        # Setup mock session
        mock_session = MagicMock()
        mock_session_class.return_value = mock_session
        
        # Mock responses
        app_infos_response = MagicMock()
        app_infos_response.status_code = 200
        app_infos_response.json.return_value = {
            'data': [{
                'id': 'info123',
                'attributes': {'appStoreState': 'DEVELOPER_REJECTED'}
            }]
        }
        
        localizations_response = MagicMock()
        localizations_response.status_code = 200
        localizations_response.json.return_value = {
            'data': [{
                'id': 'loc123',
                'attributes': {'locale': 'en-US', 'name': 'Old Name'}
            }]
        }
        
        update_response = MagicMock()
        update_response.status_code = 200
        update_response.json.return_value = {
            'data': {
                'id': 'loc123',
                'attributes': {'locale': 'en-US', 'name': 'New Name'}
            }
        }
        
        mock_session.request.side_effect = [
            app_infos_response,
            localizations_response,
            update_response
        ]
        
        # Create client and test workflow
        client = Client(
            key_id='TEST_KEY',
            issuer_id='TEST_ISSUER',
            private_key_path='/test/key.p8'
        )
        
        # Update localizations
        results = client.update_app_localizations('app123', {
            'en-US': {'name': 'New Name', 'subtitle': 'New Subtitle'}
        })
        
        # Verify results
        self.assertIn('en-US', results)
        self.assertTrue(results['en-US']['success'])
    
    @patch('app_store_connect.auth.Path.exists', return_value=True)
    @patch('builtins.open')
    @patch('app_store_connect.base.requests.Session')
    def test_error_handling_workflow(self, mock_session_class, mock_open, mock_exists):
        """Test error handling in workflow"""
        # Setup mock private key
        mock_open.return_value.__enter__.return_value.read.return_value = "mock_key"
        
        # Setup mock session
        mock_session = MagicMock()
        mock_session_class.return_value = mock_session
        
        # Mock error response
        error_response = MagicMock()
        error_response.status_code = 409
        error_response.json.return_value = {
            'errors': [{
                'title': 'The provided name is already in use'
            }]
        }
        
        mock_session.request.return_value = error_response
        
        # Create client
        client = Client(
            key_id='TEST_KEY',
            issuer_id='TEST_ISSUER',
            private_key_path='/test/key.p8'
        )
        
        # Test that error is properly raised
        from app_store_connect.exceptions import ConflictError
        
        with self.assertRaises(ConflictError) as context:
            client.apps.get('app123')
        
        self.assertIn("already in use", str(context.exception))


if __name__ == '__main__':
    # Run tests
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add mocked tests (always run)
    suite.addTests(loader.loadTestsFromTestCase(TestMockedIntegration))
    
    # Add integration tests (only if credentials available)
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
