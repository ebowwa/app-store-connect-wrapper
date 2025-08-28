"""
Apps API module for App Store Connect
"""

from typing import Dict, Any, Optional, List
from ..base import BaseAPI


class AppsAPI(BaseAPI):
    """
    Manage apps in App Store Connect
    """
    
    def get_all(self, limit: int = 200) -> List[Dict[str, Any]]:
        """
        Get all apps
        
        Args:
            limit: Number of results per page
            
        Returns:
            List of app data
        """
        return self.get_all_pages('apps', limit=limit)
    
    def get(self, app_id: str) -> Dict[str, Any]:
        """
        Get a specific app
        
        Args:
            app_id: The app ID
            
        Returns:
            App data
        """
        response = super().get(f'apps/{app_id}')
        return response['data']
    
    def get_by_bundle_id(self, bundle_id: str) -> Optional[Dict[str, Any]]:
        """
        Get app by bundle ID
        
        Args:
            bundle_id: The bundle identifier
            
        Returns:
            App data or None if not found
        """
        response = super().get('apps', params={'filter[bundleId]': bundle_id})
        data = response.get('data', [])
        return data[0] if data else None
    
    def update(self, app_id: str, **attributes) -> Dict[str, Any]:
        """
        Update app attributes
        
        Args:
            app_id: The app ID
            **attributes: Attributes to update
            
        Returns:
            Updated app data
        """
        data = {
            'data': {
                'type': 'apps',
                'id': app_id,
                'attributes': attributes
            }
        }
        response = self.patch(f'apps/{app_id}', data=data)
        return response['data']
    
    def get_app_infos(self, app_id: str) -> List[Dict[str, Any]]:
        """
        Get app info records for an app
        
        Args:
            app_id: The app ID
            
        Returns:
            List of app info data
        """
        response = super().get(f'apps/{app_id}/appInfos')
        return response.get('data', [])
    
    def get_app_store_versions(self, app_id: str) -> List[Dict[str, Any]]:
        """
        Get app store versions for an app
        
        Args:
            app_id: The app ID
            
        Returns:
            List of app store version data
        """
        response = super().get(f'apps/{app_id}/appStoreVersions')
        return response.get('data', [])
    
    def get_builds(self, app_id: str) -> List[Dict[str, Any]]:
        """
        Get builds for an app
        
        Args:
            app_id: The app ID
            
        Returns:
            List of build data
        """
        response = super().get(f'apps/{app_id}/builds')
        return response.get('data', [])