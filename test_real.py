#!/usr/bin/env python3
"""
Real integration test for App Store Connect API wrapper
Run with: uv run test_real.py
"""

import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from app_store_connect import Client


def test_real_api():
    """Test with real App Store Connect API"""
    
    # Load environment variables
    env_path = Path(__file__).parent.parent.parent / '.env'
    if env_path.exists():
        load_dotenv(env_path)
        print(f"✓ Loaded environment from {env_path}")
    else:
        print(f"⚠ No .env file at {env_path}")
    
    # Fix the auth key path
    os.environ['ASC_PRIVATE_KEY_PATH'] = '/Users/ebowwa/apps/ios/CleanShot-Exif-Scrub/AuthKey_4U9JZZ86U8.p8'
    
    # Create client
    print("\n1. Creating client...")
    try:
        client = Client.from_env()
        print("✓ Client created successfully")
    except Exception as e:
        print(f"✗ Failed to create client: {e}")
        return
    
    # Get app ID
    app_id = os.getenv('ASC_APP_ID', '6745844477')
    print(f"\n2. Using app ID: {app_id}")
    
    # Test 1: Get app
    print("\n3. Getting app details...")
    try:
        app = client.apps.get(app_id)
        print(f"✓ App found: {app['attributes']['name']} ({app['attributes']['bundleId']})")
    except Exception as e:
        print(f"✗ Failed to get app: {e}")
        return
    
    # Test 2: Get app infos
    print("\n4. Getting app infos...")
    try:
        app_infos = client.apps.get_app_infos(app_id)
        print(f"✓ Found {len(app_infos)} app info(s)")
        for info in app_infos:
            state = info.get('attributes', {}).get('appStoreState', 'Unknown')
            print(f"   - App info {info['id']}: state={state}")
    except Exception as e:
        print(f"✗ Failed to get app infos: {e}")
        return
    
    # Test 3: Get localizations
    print("\n5. Getting localizations...")
    if app_infos:
        app_info_id = app_infos[0]['id']
        try:
            localizations = client.localizations.get_all(app_info_id)
            print(f"✓ Found {len(localizations)} localization(s)")
            for loc in localizations[:5]:  # Show first 5
                locale = loc['attributes']['locale']
                name = loc['attributes'].get('name', 'N/A')
                print(f"   - {locale}: {name}")
        except Exception as e:
            print(f"✗ Failed to get localizations: {e}")
    
    # Test 4: Get versions
    print("\n6. Getting app store versions...")
    try:
        versions = client.versions.get_all(app_id)
        print(f"✓ Found {len(versions)} version(s)")
        for version in versions[:3]:  # Show first 3
            ver_str = version['attributes']['versionString']
            state = version['attributes'].get('appStoreState', 'Unknown')
            print(f"   - Version {ver_str}: {state}")
    except Exception as e:
        print(f"✗ Failed to get versions: {e}")
    
    # Test 5: Get current version
    print("\n7. Getting current version...")
    try:
        current = client.get_current_version(app_id)
        if current:
            ver_str = current['attributes']['versionString']
            state = current['attributes'].get('appStoreState', 'Unknown')
            print(f"✓ Current version: {ver_str} ({state})")
        else:
            print("✓ No current version found")
    except Exception as e:
        print(f"✗ Failed to get current version: {e}")
    
    print("\n✅ All tests completed!")


if __name__ == '__main__':
    test_real_api()