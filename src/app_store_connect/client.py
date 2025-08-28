"""
Main client for App Store Connect API
"""

from typing import Optional, Dict, Any
from pathlib import Path

from .auth import Auth
from .api.apps import AppsAPI
from .api.localizations import LocalizationsAPI, AppStoreVersionLocalizationsAPI
from .api.versions import VersionsAPI
from .api.media import MediaAPI


class Client:
    """
    Main client for interacting with App Store Connect API
    
    Example:
        >>> from app_store_connect import Client
        >>> client = Client(
        ...     key_id='YOUR_KEY_ID',
        ...     issuer_id='YOUR_ISSUER_ID',
        ...     private_key_path='/path/to/AuthKey_YOUR_KEY_ID.p8'
        ... )
        >>> apps = client.apps.get_all()
    """
    
    def __init__(
        self,
        key_id: str,
        issuer_id: str,
        private_key_path: str,
        auth: Optional[Auth] = None
    ):
        """
        Initialize the App Store Connect client
        
        Args:
            key_id: Your App Store Connect API Key ID
            issuer_id: Your App Store Connect Issuer ID
            private_key_path: Path to your .p8 private key file
            auth: Optional Auth instance (if not provided, one will be created)
        """
        if auth:
            self._auth = auth
        else:
            self._auth = Auth(key_id, issuer_id, private_key_path)
        
        # Initialize API modules
        self.apps = AppsAPI(self._auth)
        self.localizations = LocalizationsAPI(self._auth)
        self.version_localizations = AppStoreVersionLocalizationsAPI(self._auth)
        self.versions = VersionsAPI(self._auth)
        self.media = MediaAPI(self._auth)
    
    @classmethod
    def from_env(cls, env_prefix: str = 'ASC') -> 'Client':
        """
        Create client from environment variables
        
        Environment variables:
            - {prefix}_KEY_ID: API Key ID
            - {prefix}_ISSUER_ID: Issuer ID
            - {prefix}_PRIVATE_KEY_PATH: Path to .p8 file
        
        Args:
            env_prefix: Prefix for environment variables (default: 'ASC')
            
        Returns:
            Configured Client instance
        """
        import os
        
        key_id = os.getenv(f'{env_prefix}_KEY_ID')
        issuer_id = os.getenv(f'{env_prefix}_ISSUER_ID')
        private_key_path = os.getenv(f'{env_prefix}_PRIVATE_KEY_PATH')
        
        if not all([key_id, issuer_id, private_key_path]):
            raise ValueError(
                f"Missing required environment variables. "
                f"Please set {env_prefix}_KEY_ID, {env_prefix}_ISSUER_ID, "
                f"and {env_prefix}_PRIVATE_KEY_PATH"
            )
        
        return cls(key_id, issuer_id, private_key_path)
    
    def get_app_by_bundle_id(self, bundle_id: str) -> Optional[Dict[str, Any]]:
        """
        Convenience method to get an app by bundle ID
        
        Args:
            bundle_id: The app's bundle identifier
            
        Returns:
            App data or None if not found
        """
        return self.apps.get_by_bundle_id(bundle_id)
    
    def update_app_localizations(
        self,
        app_id: str,
        localizations: Dict[str, Dict[str, Any]]
    ) -> Dict[str, Dict[str, Any]]:
        """
        Convenience method to update all localizations for an app
        
        Args:
            app_id: The app ID
            localizations: Dict mapping locale to localization attributes
            
        Returns:
            Results dict mapping locale to success/error
        """
        # Get the app info
        app_infos = self.apps.get_app_infos(app_id)
        if not app_infos:
            raise ValueError(f"No app info found for app {app_id}")
        
        # Use the first available app info
        app_info_id = app_infos[0]['id']
        
        # Bulk update localizations
        return self.localizations.bulk_update(app_info_id, localizations)
    
    def get_current_version(self, app_id: str) -> Optional[Dict[str, Any]]:
        """
        Get the current version of an app
        
        Args:
            app_id: The app ID
            
        Returns:
            Current version data or None
        """
        return self.versions.get_current(app_id)
    
    def create_new_version(
        self,
        app_id: str,
        version_string: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Create a new version for an app
        
        Args:
            app_id: The app ID
            version_string: Version number (e.g., '1.0.1')
            **kwargs: Additional version attributes
            
        Returns:
            Created version data
        """
        return self.versions.create(app_id, version_string, **kwargs)
    
    def submit_for_review(self, version_id: str) -> Dict[str, Any]:
        """
        Submit a version for App Store review
        
        Args:
            version_id: The version ID
            
        Returns:
            Submission response data
        """
        return self.versions.submit_for_review(version_id)