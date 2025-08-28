"""
App Info Localizations API module for App Store Connect
"""

from typing import Dict, Any, List, Optional
from ..base import BaseAPI


class LocalizationsAPI(BaseAPI):
    """
    Manage app info localizations in App Store Connect
    """
    
    def get_all(self, app_info_id: str) -> List[Dict[str, Any]]:
        """
        Get all localizations for an app info
        
        Args:
            app_info_id: The app info ID
            
        Returns:
            List of localization data
        """
        response = self.get(f'appInfos/{app_info_id}/appInfoLocalizations')
        return response.get('data', [])
    
    def get(self, localization_id: str) -> Dict[str, Any]:
        """
        Get a specific app info localization
        
        Args:
            localization_id: The localization ID
            
        Returns:
            Localization data
        """
        response = super().get(f'appInfoLocalizations/{localization_id}')
        return response['data']
    
    def create(
        self,
        app_info_id: str,
        locale: str,
        name: Optional[str] = None,
        subtitle: Optional[str] = None,
        privacy_policy_url: Optional[str] = None,
        privacy_policy_text: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a new app info localization
        
        Args:
            app_info_id: The app info ID
            locale: The locale (e.g., 'en-US', 'fr-FR')
            name: App name for this locale
            subtitle: App subtitle for this locale
            privacy_policy_url: Privacy policy URL
            privacy_policy_text: Privacy policy text
            
        Returns:
            Created localization data
        """
        attributes = {'locale': locale}
        if name:
            attributes['name'] = name
        if subtitle:
            attributes['subtitle'] = subtitle
        if privacy_policy_url:
            attributes['privacyPolicyUrl'] = privacy_policy_url
        if privacy_policy_text:
            attributes['privacyPolicyText'] = privacy_policy_text
        
        data = {
            'data': {
                'type': 'appInfoLocalizations',
                'attributes': attributes,
                'relationships': {
                    'appInfo': {
                        'data': {
                            'type': 'appInfos',
                            'id': app_info_id
                        }
                    }
                }
            }
        }
        
        response = self.post('appInfoLocalizations', data=data)
        return response['data']
    
    def update(
        self,
        localization_id: str,
        name: Optional[str] = None,
        subtitle: Optional[str] = None,
        privacy_policy_url: Optional[str] = None,
        privacy_policy_text: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Update an app info localization
        
        Args:
            localization_id: The localization ID
            name: App name for this locale
            subtitle: App subtitle for this locale
            privacy_policy_url: Privacy policy URL
            privacy_policy_text: Privacy policy text
            
        Returns:
            Updated localization data
        """
        attributes = {}
        if name is not None:
            attributes['name'] = name
        if subtitle is not None:
            attributes['subtitle'] = subtitle
        if privacy_policy_url is not None:
            attributes['privacyPolicyUrl'] = privacy_policy_url
        if privacy_policy_text is not None:
            attributes['privacyPolicyText'] = privacy_policy_text
        
        data = {
            'data': {
                'type': 'appInfoLocalizations',
                'id': localization_id,
                'attributes': attributes
            }
        }
        
        response = self.patch(f'appInfoLocalizations/{localization_id}', data=data)
        return response['data']
    
    def delete(self, localization_id: str) -> None:
        """
        Delete an app info localization
        
        Args:
            localization_id: The localization ID
        """
        super().delete(f'appInfoLocalizations/{localization_id}')
    
    def bulk_update(
        self,
        app_info_id: str,
        localizations: Dict[str, Dict[str, Any]]
    ) -> Dict[str, Dict[str, Any]]:
        """
        Bulk update localizations for an app
        
        Args:
            app_info_id: The app info ID
            localizations: Dict mapping locale to attributes
                Example: {
                    'en-US': {'name': 'My App', 'subtitle': 'Great App'},
                    'fr-FR': {'name': 'Mon App', 'subtitle': 'Super App'}
                }
                
        Returns:
            Dict mapping locale to result (success/error)
        """
        # Get existing localizations
        existing = self.get_all(app_info_id)
        existing_by_locale = {
            loc['attributes']['locale']: loc 
            for loc in existing
        }
        
        results = {}
        
        for locale, attributes in localizations.items():
            try:
                if locale in existing_by_locale:
                    # Update existing
                    localization_id = existing_by_locale[locale]['id']
                    result = self.update(localization_id, **attributes)
                    results[locale] = {
                        'success': True,
                        'action': 'updated',
                        'data': result
                    }
                else:
                    # Create new
                    result = self.create(app_info_id, locale, **attributes)
                    results[locale] = {
                        'success': True,
                        'action': 'created',
                        'data': result
                    }
            except Exception as e:
                results[locale] = {
                    'success': False,
                    'error': str(e)
                }
        
        return results


class AppStoreVersionLocalizationsAPI(BaseAPI):
    """
    Manage app store version localizations
    """
    
    def get_all(self, version_id: str) -> List[Dict[str, Any]]:
        """
        Get all localizations for an app store version
        
        Args:
            version_id: The app store version ID
            
        Returns:
            List of localization data
        """
        response = self.get(f'appStoreVersions/{version_id}/appStoreVersionLocalizations')
        return response.get('data', [])
    
    def get(self, localization_id: str) -> Dict[str, Any]:
        """
        Get a specific app store version localization
        
        Args:
            localization_id: The localization ID
            
        Returns:
            Localization data
        """
        response = super().get(f'appStoreVersionLocalizations/{localization_id}')
        return response['data']
    
    def create(
        self,
        version_id: str,
        locale: str,
        description: Optional[str] = None,
        keywords: Optional[str] = None,
        marketing_url: Optional[str] = None,
        promotional_text: Optional[str] = None,
        support_url: Optional[str] = None,
        whats_new: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a new app store version localization
        
        Args:
            version_id: The app store version ID
            locale: The locale (e.g., 'en-US', 'fr-FR')
            description: App description
            keywords: App keywords (comma-separated)
            marketing_url: Marketing URL
            promotional_text: Promotional text
            support_url: Support URL
            whats_new: What's new text
            
        Returns:
            Created localization data
        """
        attributes = {'locale': locale}
        if description:
            attributes['description'] = description
        if keywords:
            attributes['keywords'] = keywords
        if marketing_url:
            attributes['marketingUrl'] = marketing_url
        if promotional_text:
            attributes['promotionalText'] = promotional_text
        if support_url:
            attributes['supportUrl'] = support_url
        if whats_new:
            attributes['whatsNew'] = whats_new
        
        data = {
            'data': {
                'type': 'appStoreVersionLocalizations',
                'attributes': attributes,
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
        
        response = self.post('appStoreVersionLocalizations', data=data)
        return response['data']
    
    def update(
        self,
        localization_id: str,
        description: Optional[str] = None,
        keywords: Optional[str] = None,
        marketing_url: Optional[str] = None,
        promotional_text: Optional[str] = None,
        support_url: Optional[str] = None,
        whats_new: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Update an app store version localization
        
        Args:
            localization_id: The localization ID
            description: App description
            keywords: App keywords (comma-separated)
            marketing_url: Marketing URL
            promotional_text: Promotional text
            support_url: Support URL
            whats_new: What's new text
            
        Returns:
            Updated localization data
        """
        attributes = {}
        if description is not None:
            attributes['description'] = description
        if keywords is not None:
            attributes['keywords'] = keywords
        if marketing_url is not None:
            attributes['marketingUrl'] = marketing_url
        if promotional_text is not None:
            attributes['promotionalText'] = promotional_text
        if support_url is not None:
            attributes['supportUrl'] = support_url
        if whats_new is not None:
            attributes['whatsNew'] = whats_new
        
        data = {
            'data': {
                'type': 'appStoreVersionLocalizations',
                'id': localization_id,
                'attributes': attributes
            }
        }
        
        response = self.patch(f'appStoreVersionLocalizations/{localization_id}', data=data)
        return response['data']
    
    def delete(self, localization_id: str) -> None:
        """
        Delete an app store version localization
        
        Args:
            localization_id: The localization ID
        """
        super().delete(f'appStoreVersionLocalizations/{localization_id}')