"""
App Store Versions API module for App Store Connect
"""

from typing import Dict, Any, List, Optional
from ..base import BaseAPI


class VersionsAPI(BaseAPI):
    """
    Manage app store versions in App Store Connect
    """
    
    def get_all(self, app_id: str) -> List[Dict[str, Any]]:
        """
        Get all app store versions for an app
        
        Args:
            app_id: The app ID
            
        Returns:
            List of version data
        """
        response = self.get(f'apps/{app_id}/appStoreVersions')
        return response.get('data', [])
    
    def get(self, version_id: str) -> Dict[str, Any]:
        """
        Get a specific app store version
        
        Args:
            version_id: The version ID
            
        Returns:
            Version data
        """
        response = super().get(f'appStoreVersions/{version_id}')
        return response['data']
    
    def get_current(self, app_id: str) -> Optional[Dict[str, Any]]:
        """
        Get the current live version or latest version in review
        
        Args:
            app_id: The app ID
            
        Returns:
            Current version data or None
        """
        versions = self.get_all(app_id)
        
        # Priority order for "current" version
        priority_states = [
            'READY_FOR_SALE',
            'PROCESSING_FOR_APP_STORE',
            'PENDING_DEVELOPER_RELEASE',
            'IN_REVIEW',
            'WAITING_FOR_REVIEW',
            'PREPARE_FOR_SUBMISSION',
            'DEVELOPER_REJECTED',
        ]
        
        for state in priority_states:
            for version in versions:
                if version['attributes'].get('appStoreState') == state:
                    return version
        
        # Return the most recent version if no priority match
        if versions:
            return versions[0]
        
        return None
    
    def create(
        self,
        app_id: str,
        version_string: str,
        platform: str = 'IOS',
        copyright: Optional[str] = None,
        release_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a new app store version
        
        Args:
            app_id: The app ID
            version_string: Version number (e.g., '1.0.0')
            platform: Platform ('IOS', 'MAC_OS', 'TV_OS')
            copyright: Copyright text
            release_type: Release type ('MANUAL', 'AFTER_APPROVAL', 'SCHEDULED')
            
        Returns:
            Created version data
        """
        attributes = {
            'versionString': version_string,
            'platform': platform
        }
        
        if copyright:
            attributes['copyright'] = copyright
        if release_type:
            attributes['releaseType'] = release_type
        
        data = {
            'data': {
                'type': 'appStoreVersions',
                'attributes': attributes,
                'relationships': {
                    'app': {
                        'data': {
                            'type': 'apps',
                            'id': app_id
                        }
                    }
                }
            }
        }
        
        response = self.post('appStoreVersions', data=data)
        return response['data']
    
    def update(
        self,
        version_id: str,
        version_string: Optional[str] = None,
        copyright: Optional[str] = None,
        release_type: Optional[str] = None,
        earliest_release_date: Optional[str] = None,
        uses_idfa: Optional[bool] = None,
        is_watch_only: Optional[bool] = None,
        downloadable: Optional[bool] = None
    ) -> Dict[str, Any]:
        """
        Update an app store version
        
        Args:
            version_id: The version ID
            version_string: Version number
            copyright: Copyright text
            release_type: Release type ('MANUAL', 'AFTER_APPROVAL', 'SCHEDULED')
            earliest_release_date: ISO 8601 date string for scheduled release
            uses_idfa: Whether app uses IDFA
            is_watch_only: Whether this is a watch-only app
            downloadable: Whether app is downloadable
            
        Returns:
            Updated version data
        """
        attributes = {}
        if version_string is not None:
            attributes['versionString'] = version_string
        if copyright is not None:
            attributes['copyright'] = copyright
        if release_type is not None:
            attributes['releaseType'] = release_type
        if earliest_release_date is not None:
            attributes['earliestReleaseDate'] = earliest_release_date
        if uses_idfa is not None:
            attributes['usesIdfa'] = uses_idfa
        if is_watch_only is not None:
            attributes['isWatchOnly'] = is_watch_only
        if downloadable is not None:
            attributes['downloadable'] = downloadable
        
        data = {
            'data': {
                'type': 'appStoreVersions',
                'id': version_id,
                'attributes': attributes
            }
        }
        
        response = self.patch(f'appStoreVersions/{version_id}', data=data)
        return response['data']
    
    def submit_for_review(self, version_id: str) -> Dict[str, Any]:
        """
        Submit a version for App Store review
        
        Args:
            version_id: The version ID
            
        Returns:
            Submission response data
        """
        data = {
            'data': {
                'type': 'appStoreVersionSubmissions',
                'relationships': {
                    'appStoreVersion': {
                        'data': {
                            'type': 'appStoreVersions',
                            'id': version_id
                        }
                    }
                }
            }
        }
        
        response = self.post('appStoreVersionSubmissions', data=data)
        return response['data']
    
    def get_build(self, version_id: str) -> Optional[Dict[str, Any]]:
        """
        Get the build associated with a version
        
        Args:
            version_id: The version ID
            
        Returns:
            Build data or None
        """
        response = self.get(f'appStoreVersions/{version_id}/build')
        data = response.get('data')
        return data if data else None
    
    def set_build(self, version_id: str, build_id: str) -> Dict[str, Any]:
        """
        Associate a build with a version
        
        Args:
            version_id: The version ID
            build_id: The build ID
            
        Returns:
            Updated relationship data
        """
        data = {
            'data': {
                'type': 'builds',
                'id': build_id
            }
        }
        
        response = self.patch(
            f'appStoreVersions/{version_id}/relationships/build',
            data=data
        )
        return response
    
    def get_phased_release(self, version_id: str) -> Optional[Dict[str, Any]]:
        """
        Get phased release information for a version
        
        Args:
            version_id: The version ID
            
        Returns:
            Phased release data or None
        """
        response = self.get(f'appStoreVersions/{version_id}/appStoreVersionPhasedRelease')
        data = response.get('data')
        return data if data else None
    
    def create_phased_release(
        self,
        version_id: str,
        phased_release_state: str = 'INACTIVE'
    ) -> Dict[str, Any]:
        """
        Create a phased release for a version
        
        Args:
            version_id: The version ID
            phased_release_state: Initial state ('INACTIVE', 'ACTIVE', 'PAUSED', 'COMPLETE')
            
        Returns:
            Created phased release data
        """
        data = {
            'data': {
                'type': 'appStoreVersionPhasedReleases',
                'attributes': {
                    'phasedReleaseState': phased_release_state
                },
                'relationships': {
                    'appStoreVersion': {
                        'data': {
                            'type': 'appStoreVersions',
                            'id': version_id
                        }
                    }
                }
            }
        }
        
        response = self.post('appStoreVersionPhasedReleases', data=data)
        return response['data']
    
    def update_phased_release(
        self,
        phased_release_id: str,
        phased_release_state: str
    ) -> Dict[str, Any]:
        """
        Update a phased release state
        
        Args:
            phased_release_id: The phased release ID
            phased_release_state: New state ('INACTIVE', 'ACTIVE', 'PAUSED', 'COMPLETE')
            
        Returns:
            Updated phased release data
        """
        data = {
            'data': {
                'type': 'appStoreVersionPhasedReleases',
                'id': phased_release_id,
                'attributes': {
                    'phasedReleaseState': phased_release_state
                }
            }
        }
        
        response = self.patch(f'appStoreVersionPhasedReleases/{phased_release_id}', data=data)
        return response['data']