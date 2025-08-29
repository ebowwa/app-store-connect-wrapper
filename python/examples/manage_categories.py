#!/usr/bin/env python3
"""
Example script to manage app categories in App Store Connect
"""

import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Add parent directory to path for development
sys.path.insert(0, str(Path(__file__).parent.parent))

from app_store_connect import Client


def main():
    """Example usage of Categories API"""
    
    # Load environment variables from parent project
    parent_env_path = Path(__file__).parent.parent.parent.parent / '.env'
    if parent_env_path.exists():
        load_dotenv(parent_env_path)
        print(f"✓ Loaded environment from: {parent_env_path}")
    
    # Also check local .env
    local_env_path = Path(__file__).parent.parent / '.env'
    if local_env_path.exists():
        load_dotenv(local_env_path, override=True)
        print(f"✓ Loaded environment from: {local_env_path}")
    
    # Set auth key path if not already set
    if not os.environ.get('ASC_PRIVATE_KEY_PATH'):
        # Look for .p8 file in parent project
        parent_dir = Path(__file__).parent.parent.parent.parent
        key_files = list(parent_dir.glob('AuthKey_*.p8'))
        if key_files:
            os.environ['ASC_PRIVATE_KEY_PATH'] = str(key_files[0])
            print(f"✓ Found auth key: {key_files[0].name}")
    
    # Create client
    try:
        client = Client.from_env()
        print("✓ Connected to App Store Connect\n")
    except Exception as e:
        print(f"✗ Failed to connect: {e}")
        return 1
    
    # Get app ID from environment
    app_id = os.getenv('ASC_APP_ID')
    if not app_id:
        print("✗ No app ID provided. Set ASC_APP_ID environment variable")
        return 1
    
    print(f"App ID: {app_id}\n")
    
    # Get app info
    print("Fetching app info...")
    app_infos = client.apps.get_app_infos(app_id)
    if not app_infos:
        print("✗ No app info found")
        return 1
    
    app_info = app_infos[0]
    app_info_id = app_info['id']
    print(f"✓ Found app info: {app_info_id}\n")
    
    # Get current categories
    print("Current Categories:")
    print("-" * 40)
    current = client.categories.get_app_categories(app_info_id)
    
    if current['primaryCategory']:
        primary = current['primaryCategory']['attributes']
        print(f"Primary Category: {primary.get('displayName', 'Unknown')}")
        if current['primarySubcategoryOne']:
            print(f"  - Subcategory 1: {current['primarySubcategoryOne']}")
        if current['primarySubcategoryTwo']:
            print(f"  - Subcategory 2: {current['primarySubcategoryTwo']}")
    else:
        print("Primary Category: Not set")
    
    if current['secondaryCategory']:
        secondary = current['secondaryCategory']['attributes']
        print(f"Secondary Category: {secondary.get('displayName', 'Unknown')}")
        if current['secondarySubcategoryOne']:
            print(f"  - Subcategory 1: {current['secondarySubcategoryOne']}")
        if current['secondarySubcategoryTwo']:
            print(f"  - Subcategory 2: {current['secondarySubcategoryTwo']}")
    else:
        print("Secondary Category: Not set")
    
    print()
    
    # List all available categories
    print("Available Categories:")
    print("-" * 40)
    categories = client.categories.get_all_categories()
    
    # Map common category IDs to display names
    category_names = {
        'PHOTO_AND_VIDEO': 'Photo & Video',
        'UTILITIES': 'Utilities',
        'PRODUCTIVITY': 'Productivity',
        'SOCIAL_NETWORKING': 'Social Networking',
        'LIFESTYLE': 'Lifestyle',
        'GRAPHICS_AND_DESIGN': 'Graphics & Design',
        'ENTERTAINMENT': 'Entertainment',
        'GAMES': 'Games',
        'BUSINESS': 'Business',
        'EDUCATION': 'Education',
        'HEALTH_AND_FITNESS': 'Health & Fitness',
        'MEDICAL': 'Medical',
        'MUSIC': 'Music',
        'NAVIGATION': 'Navigation',
        'NEWS': 'News',
        'REFERENCE': 'Reference',
        'SHOPPING': 'Shopping',
        'SPORTS': 'Sports',
        'TRAVEL': 'Travel',
        'WEATHER': 'Weather',
        'BOOKS': 'Books',
        'FINANCE': 'Finance',
        'FOOD_AND_DRINK': 'Food & Drink',
        'MAGAZINES_AND_NEWSPAPERS': 'Magazines & Newspapers',
        'DEVELOPER_TOOLS': 'Developer Tools',
        'STICKERS': 'Stickers'
    }
    
    # Group by parent (main categories vs subcategories)
    main_categories = []
    
    for category in categories:
        attrs = category.get('attributes', {})
        cat_id = category['id']
        # Main categories don't have a parent
        parent_id = category.get('relationships', {}).get('parent', {}).get('data')
        if not parent_id and not cat_id.startswith('GAMES_') and not cat_id.startswith('STICKERS_'):
            display_name = category_names.get(cat_id, cat_id)
            main_categories.append({
                'id': cat_id,
                'name': display_name,
                'platforms': attrs.get('platforms', [])
            })
    
    # Sort and display
    main_categories.sort(key=lambda x: x['name'])
    for cat in main_categories:
        print(f"• {cat['name']} (ID: {cat['id']})")
    
    print()
    
    # Example: Set CleanShot to Photo & Video category
    print("Example: Setting app to Photo & Video category...")
    try:
        result = client.categories.set_photo_video_category(app_info_id)
        print("✓ Successfully updated to Photo & Video category")
    except Exception as e:
        print(f"✗ Failed to update category: {e}")
    
    print()
    
    # Example: Update with specific categories
    print("Example: Setting categories directly by ID...")
    
    # You can update categories like this:
    # client.categories.update_app_categories(
    #     app_info_id=app_info_id,
    #     primary_category_id='PHOTO_AND_VIDEO',
    #     secondary_category_id='UTILITIES'
    # )
    
    print("✓ Photo & Video category ID: PHOTO_AND_VIDEO")
    print("✓ Utilities category ID: UTILITIES")
    
    print("\nDone!")
    return 0


if __name__ == '__main__':
    sys.exit(main())
