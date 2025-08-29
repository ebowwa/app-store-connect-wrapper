#!/usr/bin/env python3
"""
Example script to update App Store Connect app subtitles (shown under app name on App Store)

This script demonstrates how to update app subtitles for all localizations.
Subtitles appear directly under the app name in the App Store.

Usage:
    1. Set environment variables:
       - ASC_KEY_ID
       - ASC_ISSUER_ID  
       - ASC_PRIVATE_KEY_PATH
       - ASC_APP_ID
    2. Run: python update_app_subtitles.py
"""

import sys
import os
from pathlib import Path
from typing import Dict, Any
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).parent.parent))

from app_store_connect import Client
from app_store_connect.api.localizations import LocalizationsAPI


# Subtitle data for each language
# NOTE: Excluding en-US as requested - don't edit the main English market
# IMPORTANT: App Store Connect limit - Subtitle: 30 characters max
SUBTITLES = {
    'de-DE': {
        'subtitle': 'Privatsphäre-Schutz'  # "Privacy Protection"
    },
    'es-ES': {
        'subtitle': 'Protección de Privacidad'  # "Privacy Protection"
    },
    'fr-FR': {
        'subtitle': 'Protection Vie Privée'  # "Privacy Protection"
    },
    'ja': {
        'subtitle': 'プライバシー保護'  # "Privacy Protection"
    },
    'ko': {
        'subtitle': '개인정보 보호'  # "Privacy Protection"
    },
    'pt-BR': {
        'subtitle': 'Proteção de Privacidade'  # "Privacy Protection"
    },
    'ru': {
        'subtitle': 'Защита Конфиденциальности'  # "Privacy Protection" (29 chars)
    },
    'zh-Hans': {
        'subtitle': '隐私保护'  # "Privacy Protection"
    },
    'zh-Hant': {
        'subtitle': '隱私保護'  # "Privacy Protection"
    },
    'ar-SA': {
        'subtitle': 'حماية الخصوصية'  # "Privacy Protection"
    },
    'hi': {
        'subtitle': 'गोपनीयता सुरक्षा'  # "Privacy Protection"
    },
    'it': {
        'subtitle': 'Protezione Privacy'  # "Privacy Protection"
    },
    'es-MX': {
        'subtitle': 'Protección de Privacidad'  # "Privacy Protection"
    }
}


def update_app_info_subtitles(client: Client, app_id: str, dry_run: bool = False) -> Dict[str, Any]:
    """
    Update App Info localizations with subtitles
    """
    results = {}
    
    # Get app infos
    print("\nFetching app info...")
    try:
        app_infos = client.apps.get_app_infos(app_id)
        if not app_infos:
            print("✗ No app info found")
            return results
        
        # Find editable app info (preferably not READY_FOR_SALE)
        app_info = None
        for info in app_infos:
            state = info.get('attributes', {}).get('appStoreState')
            # Use editable states first
            if state in ['DEVELOPER_REJECTED', 'PREPARE_FOR_SUBMISSION', 'METADATA_REJECTED']:
                app_info = info
                print(f"✓ Using editable app info: {info['id']} (state: {state})")
                break
        
        # Fallback to any app info if no editable one found
        if not app_info:
            app_info = app_infos[0]
            state = app_info.get('attributes', {}).get('appStoreState')
            print(f"⚠ Using app info: {app_info['id']} (state: {state}) - may not be editable")
        
        app_info_id = app_info['id']
        
    except Exception as e:
        print(f"✗ Failed to get app info: {e}")
        return results
    
    # Get existing app info localizations
    print("\nFetching existing app info localizations...")
    try:
        # Create the API instance using client's auth
        localizations_api = LocalizationsAPI(auth=client._auth)
        localizations = localizations_api.get_all(app_info_id)
        print(f"✓ Found {len(localizations)} app info localization(s)")
        
        # Create locale to ID mapping
        locale_map = {}
        for loc in localizations:
            locale = loc['attributes']['locale']
            locale_map[locale] = loc['id']
            current_subtitle = loc['attributes'].get('subtitle', 'None')
            print(f"  - {locale}: current subtitle = '{current_subtitle}'")
            
    except Exception as e:
        print(f"✗ Failed to get app info localizations: {e}")
        return results
    
    # Update each localization with subtitle
    print(f"\n{'[DRY RUN] ' if dry_run else ''}Updating app info subtitles...")
    
    for locale, content in SUBTITLES.items():
        print(f"\n  Processing {locale}...")
        
        subtitle = content.get('subtitle')
        if not subtitle:
            continue
            
        if dry_run:
            print(f"    [DRY RUN] Would update subtitle to: '{subtitle}' ({len(subtitle)} chars)")
            results[locale] = {'success': True, 'action': 'dry_run'}
            continue
        
        try:
            if locale in locale_map:
                # Update existing localization
                loc_id = locale_map[locale]
                print(f"    Updating existing localization (ID: {loc_id})...")
                print(f"    Setting subtitle: '{subtitle}' ({len(subtitle)} chars)")
                
                result = localizations_api.update(
                    loc_id,
                    subtitle=subtitle
                )
                
                print(f"    ✓ Updated successfully")
                results[locale] = {'success': True, 'action': 'updated', 'data': result}
                
            else:
                # Create new localization
                print(f"    Creating new localization...")
                print(f"    Setting subtitle: '{subtitle}' ({len(subtitle)} chars)")
                
                result = localizations_api.create(
                    app_info_id,
                    locale,
                    subtitle=subtitle
                )
                
                print(f"    ✓ Created successfully")
                results[locale] = {'success': True, 'action': 'created', 'data': result}
                
        except Exception as e:
            print(f"    ✗ Failed: {e}")
            results[locale] = {'success': False, 'error': str(e)}
    
    return results


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Update App Store Connect subtitles')
    parser.add_argument('--app-id', help='App ID (defaults to env var ASC_APP_ID)')
    parser.add_argument('--dry-run', action='store_true', help='Simulate updates without making changes')
    
    args = parser.parse_args()
    
    # Load environment
    env_path = Path(__file__).parent.parent.parent / '.env'
    if env_path.exists():
        load_dotenv(env_path)
    
    # Set auth key path if not already set
    if not os.environ.get('ASC_PRIVATE_KEY_PATH'):
        # Look for .p8 file in parent directories
        key_path = Path(__file__).parent.parent.parent / 'AuthKey_*.p8'
        key_files = list(Path(__file__).parent.parent.parent.glob('AuthKey_*.p8'))
        if key_files:
            os.environ['ASC_PRIVATE_KEY_PATH'] = str(key_files[0])
    
    # Create client
    try:
        client = Client.from_env()
        print("✓ Connected to App Store Connect")
    except Exception as e:
        print(f"✗ Failed to connect: {e}")
        return 1
    
    # Get app ID
    app_id = args.app_id or os.getenv('ASC_APP_ID')
    if not app_id:
        print("✗ No app ID provided. Set ASC_APP_ID environment variable or use --app-id")
        return 1
    print(f"\nApp ID: {app_id}")
    
    # Update subtitles
    results = update_app_info_subtitles(client, app_id, args.dry_run)
    
    # Summary
    print("\n" + "="*50)
    print("Summary:")
    success_count = sum(1 for r in results.values() if r.get('success'))
    failed_count = len(results) - success_count
    
    print(f"  Success: {success_count}")
    print(f"  Failed: {failed_count}")
    
    if failed_count > 0:
        print("\nFailed locales:")
        for locale, result in results.items():
            if not result.get('success'):
                print(f"  - {locale}: {result.get('error')}")
    
    return 0 if failed_count == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
