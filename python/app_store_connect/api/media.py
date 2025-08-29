"""
Media and Assets API module for App Store Connect
Handles screenshots and app previews

NOTE: App icon functionality has been removed as Apple does not support
localized app icons. All regions use the same global app icon.
"""

from typing import Dict, Any, List, Optional, BinaryIO
from pathlib import Path
import mimetypes
from ..base import BaseAPI


class MediaAPI(BaseAPI):
    """
    Manage app media assets in App Store Connect
    """
    
    # App Icons - REMOVED
    # NOTE: Apple App Store Connect does not support localized app icons.
    # All regions/localizations use the same global app icon.
    # The app icon is uploaded once through Xcode or App Store Connect web interface.
    # 
    # If Apple adds this feature in the future, implement these methods:
    # - get_app_icons(app_info_id) - Get app icons
    # - upload_app_icon(app_info_localization_id, file_path, file_size) - Upload icon
    #
    # The API endpoints would be:
    # - GET /appInfos/{id}/appInfoLocalizations
    # - POST /appInfoLocalizationAppIcons
    # - PATCH /appInfoLocalizationAppIcons/{id}
    
    # Screenshots
    
    def get_screenshots(
        self,
        localization_id: str,
        display_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get screenshots for an app store version localization
        
        Args:
            localization_id: The app store version localization ID
            display_type: Optional display type filter (e.g., 'APP_IPHONE_65', 'APP_IPHONE_58')
            
        Returns:
            List of screenshot data
        """
        endpoint = f'appStoreVersionLocalizations/{localization_id}/appScreenshotSets'
        
        if display_type:
            endpoint += f'?filter[screenshotDisplayType]={display_type}'
        
        response = super().get(endpoint)
        screenshot_sets = response.get('data', [])
        
        # Get screenshots for each set
        all_screenshots = []
        for set_data in screenshot_sets:
            set_id = set_data['id']
            screenshots_response = super().get(f'appScreenshotSets/{set_id}/appScreenshots')
            screenshots = screenshots_response.get('data', [])
            
            for screenshot in screenshots:
                screenshot['displayType'] = set_data['attributes']['screenshotDisplayType']
                all_screenshots.append(screenshot)
        
        return all_screenshots
    
    def create_screenshot_set(
        self,
        localization_id: str,
        display_type: str
    ) -> Dict[str, Any]:
        """
        Create a screenshot set for a specific display type
        
        Args:
            localization_id: The app store version localization ID
            display_type: Display type (e.g., 'APP_IPHONE_65', 'APP_IPHONE_58', 'APP_IPAD_PRO_129')
            
        Returns:
            Created screenshot set data
        """
        data = {
            'data': {
                'type': 'appScreenshotSets',
                'attributes': {
                    'screenshotDisplayType': display_type
                },
                'relationships': {
                    'appStoreVersionLocalization': {
                        'data': {
                            'type': 'appStoreVersionLocalizations',
                            'id': localization_id
                        }
                    }
                }
            }
        }
        
        response = super().post('appScreenshotSets', data=data)
        return response['data']
    
    def upload_screenshot(
        self,
        screenshot_set_id: str,
        file_path: str,
        file_size: int,
        width: int,
        height: int
    ) -> Dict[str, Any]:
        """
        Reserve a screenshot upload
        
        Args:
            screenshot_set_id: The screenshot set ID
            file_path: Path to the screenshot file
            file_size: Size of the file in bytes
            width: Image width in pixels
            height: Image height in pixels
            
        Returns:
            Screenshot reservation data with upload details
        """
        data = {
            'data': {
                'type': 'appScreenshots',
                'attributes': {
                    'fileSize': file_size,
                    'fileName': Path(file_path).name,
                    'sourceFileChecksum': '',  # Calculate MD5 if needed
                    'imageAsset': {
                        'width': width,
                        'height': height
                    }
                },
                'relationships': {
                    'appScreenshotSet': {
                        'data': {
                            'type': 'appScreenshotSets',
                            'id': screenshot_set_id
                        }
                    }
                }
            }
        }
        
        response = super().post('appScreenshots', data=data)
        return response['data']
    
    def reorder_screenshots(
        self,
        screenshot_set_id: str,
        screenshot_ids: List[str]
    ) -> Dict[str, Any]:
        """
        Reorder screenshots within a set
        
        Args:
            screenshot_set_id: The screenshot set ID
            screenshot_ids: Ordered list of screenshot IDs
            
        Returns:
            Updated screenshot set
        """
        data = {
            'data': [
                {'type': 'appScreenshots', 'id': screenshot_id}
                for screenshot_id in screenshot_ids
            ]
        }
        
        response = super().patch(
            f'appScreenshotSets/{screenshot_set_id}/relationships/appScreenshots',
            data=data
        )
        return response
    
    def delete_screenshot(self, screenshot_id: str) -> None:
        """
        Delete a screenshot
        
        Args:
            screenshot_id: The screenshot ID
        """
        super().delete(f'appScreenshots/{screenshot_id}')
    
    # App Previews (Videos)
    
    def get_app_previews(
        self,
        localization_id: str,
        display_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get app preview videos for an app store version localization
        
        Args:
            localization_id: The app store version localization ID
            display_type: Optional display type filter
            
        Returns:
            List of app preview data
        """
        endpoint = f'appStoreVersionLocalizations/{localization_id}/appPreviewSets'
        
        if display_type:
            endpoint += f'?filter[previewType]={display_type}'
        
        response = super().get(endpoint)
        preview_sets = response.get('data', [])
        
        all_previews = []
        for set_data in preview_sets:
            set_id = set_data['id']
            previews_response = super().get(f'appPreviewSets/{set_id}/appPreviews')
            previews = previews_response.get('data', [])
            
            for preview in previews:
                preview['displayType'] = set_data['attributes']['previewType']
                all_previews.append(preview)
        
        return all_previews
    
    def create_preview_set(
        self,
        localization_id: str,
        preview_type: str
    ) -> Dict[str, Any]:
        """
        Create an app preview set for a specific display type
        
        Args:
            localization_id: The app store version localization ID
            preview_type: Preview type (e.g., 'IPHONE_65', 'IPHONE_58', 'IPAD_PRO_129')
            
        Returns:
            Created preview set data
        """
        data = {
            'data': {
                'type': 'appPreviewSets',
                'attributes': {
                    'previewType': preview_type
                },
                'relationships': {
                    'appStoreVersionLocalization': {
                        'data': {
                            'type': 'appStoreVersionLocalizations',
                            'id': localization_id
                        }
                    }
                }
            }
        }
        
        response = super().post('appPreviewSets', data=data)
        return response['data']
    
    def upload_preview(
        self,
        preview_set_id: str,
        file_path: str,
        file_size: int,
        preview_frame_time_code: str = '00:00:05:00'
    ) -> Dict[str, Any]:
        """
        Reserve an app preview video upload
        
        Args:
            preview_set_id: The preview set ID
            file_path: Path to the video file
            file_size: Size of the file in bytes
            preview_frame_time_code: Timecode for preview frame (default: 5 seconds)
            
        Returns:
            Preview reservation data with upload details
        """
        data = {
            'data': {
                'type': 'appPreviews',
                'attributes': {
                    'fileSize': file_size,
                    'fileName': Path(file_path).name,
                    'previewFrameTimeCode': preview_frame_time_code,
                    'sourceFileChecksum': ''  # Calculate MD5 if needed
                },
                'relationships': {
                    'appPreviewSet': {
                        'data': {
                            'type': 'appPreviewSets',
                            'id': preview_set_id
                        }
                    }
                }
            }
        }
        
        response = super().post('appPreviews', data=data)
        return response['data']
    
    # Helper methods for complete upload workflow
    
    def complete_asset_upload(
        self,
        asset_id: str,
        asset_type: str,
        uploaded: bool = True,
        source_file_checksum: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Mark an asset upload as complete
        
        Args:
            asset_id: The asset ID (screenshot or preview ID)
            asset_type: Type of asset ('appScreenshots' or 'appPreviews')
            uploaded: Whether the upload completed successfully
            source_file_checksum: MD5 checksum of the uploaded file
            
        Returns:
            Updated asset data
        """
        data = {
            'data': {
                'type': asset_type,
                'id': asset_id,
                'attributes': {
                    'uploaded': uploaded
                }
            }
        }
        
        if source_file_checksum:
            data['data']['attributes']['sourceFileChecksum'] = source_file_checksum
        
        response = super().patch(f'{asset_type}/{asset_id}', data=data)
        return response['data']
    
    @staticmethod
    def get_display_types() -> Dict[str, List[str]]:
        """
        Get available display types for screenshots and previews
        
        Returns:
            Dictionary of device categories and their display types
        """
        return {
            'iphone': [
                'APP_IPHONE_65',      # iPhone 6.5" (iPhone 14 Pro Max, 13 Pro Max, 12 Pro Max, 11 Pro Max, XS Max)
                'APP_IPHONE_61',      # iPhone 6.1" (iPhone 14 Pro, 14, 13 Pro, 13, 12 Pro, 12, 11, XR)
                'APP_IPHONE_58',      # iPhone 5.8" (iPhone 13 mini, 12 mini, 11 Pro, XS, X)
                'APP_IPHONE_55',      # iPhone 5.5" (iPhone 8 Plus, 7 Plus, 6s Plus, 6 Plus)
                'APP_IPHONE_47',      # iPhone 4.7" (iPhone SE 3rd/2nd gen, 8, 7, 6s, 6)
                'APP_IPHONE_40',      # iPhone 4" (iPhone SE 1st gen, 5s, 5c, 5)
                'APP_IPHONE_35',      # iPhone 3.5" (iPhone 4s, 4, 3GS)
            ],
            'ipad': [
                'APP_IPAD_PRO_129',   # iPad Pro 12.9" (6th, 5th, 4th, 3rd, 2nd, 1st gen)
                'APP_IPAD_PRO_3GEN_129',  # iPad Pro 12.9" (3rd gen)
                'APP_IPAD_PRO_3GEN_11',   # iPad Pro 11" 
                'APP_IPAD_105',       # iPad 10.5" (Air 3rd gen, Pro 10.5")
                'APP_IPAD_97',        # iPad 9.7" (6th, 5th gen, Air 2, Air, Pro 9.7")
            ],
            'apple_tv': [
                'APP_APPLE_TV',       # Apple TV
            ],
            'apple_watch': [
                'APP_WATCH_ULTRA',    # Apple Watch Ultra
                'APP_WATCH_SERIES_7', # Apple Watch Series 7
                'APP_WATCH_SERIES_4', # Apple Watch Series 4-6, SE
                'APP_WATCH_SERIES_3', # Apple Watch Series 3
            ],
            'mac': [
                'APP_DESKTOP',        # Mac
            ]
        }