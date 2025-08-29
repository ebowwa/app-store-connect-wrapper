"""
App Categories API module for App Store Connect
Manages primary and secondary app categories
"""

from typing import Dict, Any, List, Optional
from ..base import BaseAPI


class CategoriesAPI(BaseAPI):
    """
    Manage app categories and subcategories in App Store Connect
    """
    
    # Available App Store Categories
    # Reference: https://developer.apple.com/app-store/categories/
    CATEGORIES = {
        'BOOKS': 'Books',
        'BUSINESS': 'Business', 
        'DEVELOPER_TOOLS': 'Developer Tools',
        'EDUCATION': 'Education',
        'ENTERTAINMENT': 'Entertainment',
        'FINANCE': 'Finance',
        'FOOD_AND_DRINK': 'Food & Drink',
        'GAMES': 'Games',
        'GRAPHICS_AND_DESIGN': 'Graphics & Design',
        'HEALTH_AND_FITNESS': 'Health & Fitness',
        'LIFESTYLE': 'Lifestyle',
        'MAGAZINES_AND_NEWSPAPERS': 'Magazines & Newspapers',
        'MEDICAL': 'Medical',
        'MUSIC': 'Music',
        'NAVIGATION': 'Navigation',
        'NEWS': 'News',
        'PHOTO_AND_VIDEO': 'Photo & Video',
        'PRODUCTIVITY': 'Productivity',
        'REFERENCE': 'Reference',
        'SHOPPING': 'Shopping',
        'SOCIAL_NETWORKING': 'Social Networking',
        'SPORTS': 'Sports',
        'TRAVEL': 'Travel',
        'UTILITIES': 'Utilities',
        'WEATHER': 'Weather'
    }
    
    # Game Subcategories
    GAME_SUBCATEGORIES = {
        'ACTION': 'Action',
        'ADVENTURE': 'Adventure',
        'ARCADE': 'Arcade',
        'BOARD': 'Board',
        'CARD': 'Card',
        'CASINO': 'Casino',
        'CASUAL': 'Casual',
        'DICE': 'Dice',
        'EDUCATIONAL': 'Educational',
        'FAMILY': 'Family',
        'MUSIC': 'Music',
        'PUZZLE': 'Puzzle',
        'RACING': 'Racing',
        'ROLE_PLAYING': 'Role Playing',
        'SIMULATION': 'Simulation',
        'SPORTS': 'Sports',
        'STRATEGY': 'Strategy',
        'TRIVIA': 'Trivia',
        'WORD': 'Word'
    }
    
    # Magazines & Newspapers Subcategories
    NEWSSTAND_SUBCATEGORIES = {
        'ARTS_AND_PHOTOGRAPHY': 'Arts & Photography',
        'AUTOMOTIVE': 'Automotive',
        'BRIDES_AND_WEDDINGS': 'Brides & Weddings',
        'BUSINESS_AND_INVESTING': 'Business & Investing',
        'CHILDRENS_MAGAZINES': "Children's Magazines",
        'COMPUTERS_AND_INTERNET': 'Computers & Internet',
        'COOKING_FOOD_AND_DRINK': 'Cooking, Food & Drink',
        'CRAFTS_AND_HOBBIES': 'Crafts & Hobbies',
        'ELECTRONICS_AND_AUDIO': 'Electronics & Audio',
        'ENTERTAINMENT': 'Entertainment',
        'FASHION_AND_STYLE': 'Fashion & Style',
        'HEALTH_MIND_AND_BODY': 'Health, Mind & Body',
        'HISTORY': 'History',
        'HOME_AND_GARDEN': 'Home & Garden',
        'LITERARY_MAGAZINES_AND_JOURNALS': 'Literary Magazines & Journals',
        'MENS_INTEREST': "Men's Interest",
        'MOVIES_AND_MUSIC': 'Movies & Music',
        'NEWS_AND_POLITICS': 'News & Politics',
        'OUTDOORS_AND_NATURE': 'Outdoors & Nature',
        'PARENTING_AND_FAMILY': 'Parenting & Family',
        'PETS': 'Pets',
        'PROFESSIONAL_AND_TRADE': 'Professional & Trade',
        'REGIONAL_NEWS': 'Regional News',
        'SCIENCE': 'Science',
        'SPORTS_AND_LEISURE': 'Sports & Leisure',
        'TEENS': 'Teens',
        'TRAVEL_AND_REGIONAL': 'Travel & Regional',
        'WOMENS_INTEREST': "Women's Interest"
    }
    
    def get_app_categories(self, app_info_id: str) -> Dict[str, Any]:
        """
        Get the current primary and secondary categories for an app
        
        Args:
            app_info_id: The app info ID
            
        Returns:
            Dictionary containing primary and secondary category information
        """
        endpoint = f'appInfos/{app_info_id}'
        params = {
            'fields[appInfos]': 'primaryCategory,secondaryCategory,primarySubcategoryOne,primarySubcategoryTwo,secondarySubcategoryOne,secondarySubcategoryTwo',
            'include': 'primaryCategory,secondaryCategory'
        }
        
        response = super().get(endpoint, params=params)
        app_info = response.get('data', {})
        
        # Extract category relationships
        relationships = app_info.get('relationships', {})
        included = response.get('included', [])
        
        # Build category lookup from included data
        category_lookup = {}
        for item in included:
            if item.get('type') == 'appCategories':
                category_lookup[item['id']] = item['attributes']
        
        # Extract current categories
        result = {
            'primaryCategory': None,
            'secondaryCategory': None,
            'primarySubcategoryOne': None,
            'primarySubcategoryTwo': None,
            'secondarySubcategoryOne': None,
            'secondarySubcategoryTwo': None
        }
        
        # Get primary category
        primary_cat = relationships.get('primaryCategory', {}).get('data')
        if primary_cat:
            result['primaryCategory'] = {
                'id': primary_cat['id'],
                'attributes': category_lookup.get(primary_cat['id'], {})
            }
        
        # Get secondary category
        secondary_cat = relationships.get('secondaryCategory', {}).get('data')
        if secondary_cat:
            result['secondaryCategory'] = {
                'id': secondary_cat['id'],
                'attributes': category_lookup.get(secondary_cat['id'], {})
            }
        
        # Get subcategories from attributes
        attributes = app_info.get('attributes', {})
        result['primarySubcategoryOne'] = attributes.get('primarySubcategoryOne')
        result['primarySubcategoryTwo'] = attributes.get('primarySubcategoryTwo')
        result['secondarySubcategoryOne'] = attributes.get('secondarySubcategoryOne')
        result['secondarySubcategoryTwo'] = attributes.get('secondarySubcategoryTwo')
        
        return result
    
    def update_app_categories(
        self,
        app_info_id: str,
        primary_category_id: Optional[str] = None,
        secondary_category_id: Optional[str] = None,
        primary_subcategory_one: Optional[str] = None,
        primary_subcategory_two: Optional[str] = None,
        secondary_subcategory_one: Optional[str] = None,
        secondary_subcategory_two: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Update app categories and subcategories
        
        Args:
            app_info_id: The app info ID
            primary_category_id: Primary category ID (use get_all_categories to find IDs)
            secondary_category_id: Optional secondary category ID
            primary_subcategory_one: First subcategory for primary category (for Games/Newsstand)
            primary_subcategory_two: Second subcategory for primary category (for Games/Newsstand)
            secondary_subcategory_one: First subcategory for secondary category
            secondary_subcategory_two: Second subcategory for secondary category
            
        Returns:
            Updated app info data
            
        Note:
            - Primary category is required for all apps
            - Secondary category is optional
            - Subcategories are only applicable for Games and Magazines & Newspapers categories
            - You can have up to 2 subcategories per category
        """
        data = {
            'data': {
                'type': 'appInfos',
                'id': app_info_id,
                'attributes': {},
                'relationships': {}
            }
        }
        
        # Add subcategories to attributes if provided
        if primary_subcategory_one is not None:
            data['data']['attributes']['primarySubcategoryOne'] = primary_subcategory_one
        if primary_subcategory_two is not None:
            data['data']['attributes']['primarySubcategoryTwo'] = primary_subcategory_two
        if secondary_subcategory_one is not None:
            data['data']['attributes']['secondarySubcategoryOne'] = secondary_subcategory_one
        if secondary_subcategory_two is not None:
            data['data']['attributes']['secondarySubcategoryTwo'] = secondary_subcategory_two
        
        # Add category relationships if provided
        if primary_category_id:
            data['data']['relationships']['primaryCategory'] = {
                'data': {
                    'type': 'appCategories',
                    'id': primary_category_id
                }
            }
        
        if secondary_category_id:
            data['data']['relationships']['secondaryCategory'] = {
                'data': {
                    'type': 'appCategories',
                    'id': secondary_category_id
                }
            }
        
        response = super().patch(f'appInfos/{app_info_id}', data=data)
        return response.get('data', {})
    
    def get_all_categories(self, platform: str = 'IOS') -> List[Dict[str, Any]]:
        """
        Get all available app categories
        
        Args:
            platform: Platform filter - IOS, MAC_OS, TV_OS (default: IOS)
            
        Returns:
            List of available categories with their IDs and attributes
        """
        endpoint = 'appCategories'
        params = {
            'filter[platforms]': platform,
            'limit': 200  # Get all categories
        }
        
        response = super().get(endpoint, params=params)
        return response.get('data', [])
    
    def get_category_by_name(self, category_name: str, platform: str = 'IOS') -> Optional[Dict[str, Any]]:
        """
        Find a category by its display name
        
        Args:
            category_name: The category display name (e.g., 'Photo & Video', 'Games')
            platform: Platform filter - IOS, MAC_OS, TV_OS (default: IOS)
            
        Returns:
            Category data if found, None otherwise
        """
        categories = self.get_all_categories(platform)
        
        for category in categories:
            # Check against the display name in attributes
            if category.get('attributes', {}).get('displayName') == category_name:
                return category
        
        return None
    
    def set_photo_video_category(self, app_info_id: str) -> Dict[str, Any]:
        """
        Convenience method to set app category to Photo & Video
        Useful for photo editing apps like CleanShot
        
        Args:
            app_info_id: The app info ID
            
        Returns:
            Updated app info data
        """
        # Photo & Video category ID is PHOTO_AND_VIDEO
        return self.update_app_categories(
            app_info_id=app_info_id,
            primary_category_id='PHOTO_AND_VIDEO'
        )
    
    def set_game_category(
        self,
        app_info_id: str,
        game_subcategory_one: str,
        game_subcategory_two: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Convenience method to set app as a game with subcategories
        
        Args:
            app_info_id: The app info ID
            game_subcategory_one: First game subcategory (from GAME_SUBCATEGORIES)
            game_subcategory_two: Optional second game subcategory
            
        Returns:
            Updated app info data
        """
        # Find Games category
        games_category = self.get_category_by_name('Games')
        if not games_category:
            raise ValueError("Games category not found")
        
        # Validate subcategories
        if game_subcategory_one not in self.GAME_SUBCATEGORIES:
            raise ValueError(f"Invalid game subcategory: {game_subcategory_one}")
        
        if game_subcategory_two and game_subcategory_two not in self.GAME_SUBCATEGORIES:
            raise ValueError(f"Invalid game subcategory: {game_subcategory_two}")
        
        return self.update_app_categories(
            app_info_id=app_info_id,
            primary_category_id=games_category['id'],
            primary_subcategory_one=game_subcategory_one,
            primary_subcategory_two=game_subcategory_two
        )