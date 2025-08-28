#!/usr/bin/env python3
"""
Example: Upload localized app icons to App Store Connect

This script demonstrates how to upload different app icons for each localization.
Note: Actual file upload to Apple's servers requires additional HTTP requests
to the upload URLs provided by the API.
"""

import sys
import os
from pathlib import Path
from typing import Dict, Optional
import hashlib
import requests

sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from app_store_connect import Client


# Localized app icon mappings (1024x1024 PNG files)
LOCALIZED_ICONS = {
    'en-US': 'icons/icon_en.png',        # English - CleanShot
    'de-DE': 'icons/icon_de.png',        # German - SauberBild
    'es-ES': 'icons/icon_es.png',        # Spanish - FotoLimpia
    'es-MX': 'icons/icon_es_mx.png',     # Spanish (Mexico) - FotoLimpia México
    'fr-FR': 'icons/icon_fr.png',        # French - PhotoPure
    'ja': 'icons/icon_ja.png',           # Japanese - クリーンショット
    'ko': 'icons/icon_ko.png',           # Korean - 클린샷
    'pt-BR': 'icons/icon_pt_br.png',     # Portuguese (Brazil) - FotoLimpa Brasil
    'ru': 'icons/icon_ru.png',           # Russian - ЧистыйСнимок
    'zh-Hans': 'icons/icon_zh_cn.png',   # Chinese Simplified - 净图
    'zh-Hant': 'icons/icon_zh_tw.png',   # Chinese Traditional - 淨圖
    'ar-SA': 'icons/icon_ar.png',        # Arabic - صورة نظيفة
    'hi': 'icons/icon_hi.png',           # Hindi - साफ़ छवि
    'it': 'icons/icon_it.png',           # Italian - Scatto Pulito
}


def calculate_md5(file_path: str) -> str:
    """Calculate MD5 checksum of a file"""
    md5 = hashlib.md5()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            md5.update(chunk)
    return md5.hexdigest()


def upload_file_to_apple(upload_url: str, file_path: str, headers: Dict[str, str]) -> bool:
    """
    Upload a file to Apple's upload URL
    
    Args:
        upload_url: The URL provided by Apple for upload
        file_path: Path to the file to upload
        headers: Headers required for the upload
        
    Returns:
        True if upload successful
    """
    with open(file_path, 'rb') as f:
        response = requests.put(
            upload_url,
            data=f,
            headers=headers
        )
    
    return response.status_code == 200


def upload_localized_icon(
    client: Client,
    app_info_localization_id: str,
    locale: str,
    icon_path: str,
    dry_run: bool = False
) -> Optional[Dict]:
    """
    Upload an app icon for a specific localization
    
    Args:
        client: App Store Connect client
        app_info_localization_id: The localization ID
        locale: The locale code
        icon_path: Path to the icon file
        dry_run: If True, only simulate the upload
        
    Returns:
        Upload result or None if failed
    """
    if not Path(icon_path).exists():
        print(f"  ✗ {locale}: Icon file not found: {icon_path}")
        return None
    
    file_size = Path(icon_path).stat().st_size
    file_name = Path(icon_path).name
    
    print(f"  Processing {locale}: {file_name} ({file_size:,} bytes)")
    
    if dry_run:
        print(f"    [DRY RUN] Would upload {icon_path}")
        return {'dry_run': True}
    
    try:
        # Step 1: Reserve the icon upload
        print(f"    Reserving upload slot...")
        reservation = client.media.upload_app_icon(
            app_info_localization_id,
            icon_path,
            file_size
        )
        
        if not reservation:
            print(f"    ✗ Failed to reserve upload slot")
            return None
        
        # Step 2: Get upload operations from reservation
        upload_operations = reservation.get('attributes', {}).get('uploadOperations', [])
        if not upload_operations:
            print(f"    ✗ No upload operations provided")
            return None
        
        # Step 3: Upload the file to each URL (usually just one)
        for operation in upload_operations:
            upload_url = operation.get('url')
            headers = operation.get('requestHeaders', {})
            
            print(f"    Uploading to Apple servers...")
            success = upload_file_to_apple(upload_url, icon_path, headers)
            
            if not success:
                print(f"    ✗ Upload failed")
                return None
        
        # Step 4: Mark upload as complete
        asset_id = reservation['id']
        checksum = calculate_md5(icon_path)
        
        print(f"    Completing upload...")
        result = client.media.complete_asset_upload(
            asset_id,
            'appInfoLocalizationAppIcons',
            uploaded=True,
            source_file_checksum=checksum
        )
        
        print(f"    ✓ {locale}: Icon uploaded successfully")
        return result
        
    except Exception as e:
        print(f"    ✗ {locale}: Error: {e}")
        return None


def main():
    """Main entry point"""
    import argparse
    from dotenv import load_dotenv
    
    parser = argparse.ArgumentParser(description='Upload localized app icons to App Store Connect')
    parser.add_argument('--app-id', help='App ID (defaults to env var ASC_APP_ID)')
    parser.add_argument('--dry-run', action='store_true', help='Simulate upload without making changes')
    parser.add_argument('--locale', help='Upload icon for specific locale only')
    parser.add_argument('--icons-dir', default='./icons', help='Directory containing icon files')
    
    args = parser.parse_args()
    
    # Load environment
    env_path = Path(__file__).parent.parent.parent.parent / '.env'
    if env_path.exists():
        load_dotenv(env_path)
    
    # Fix auth key path
    os.environ['ASC_PRIVATE_KEY_PATH'] = '/Users/ebowwa/apps/ios/CleanShot-Exif-Scrub/AuthKey_4U9JZZ86U8.p8'
    
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
        print("✗ No app ID provided")
        return 1
    
    print(f"\nApp ID: {app_id}")
    
    # Get app infos
    print("\nFetching app info...")
    try:
        app_infos = client.apps.get_app_infos(app_id)
        if not app_infos:
            print("✗ No app info found")
            return 1
        
        # Find editable app info
        app_info = None
        for info in app_infos:
            state = info.get('attributes', {}).get('appStoreState')
            if state in ['DEVELOPER_REJECTED', 'PREPARE_FOR_SUBMISSION', 'METADATA_REJECTED']:
                app_info = info
                print(f"✓ Using editable app info: {info['id']} (state: {state})")
                break
        
        if not app_info:
            app_info = app_infos[0]
            state = app_info.get('attributes', {}).get('appStoreState')
            print(f"⚠ Using app info: {app_info['id']} (state: {state}) - may not be editable")
        
    except Exception as e:
        print(f"✗ Failed to get app info: {e}")
        return 1
    
    # Get localizations
    print("\nFetching localizations...")
    try:
        localizations = client.localizations.get_all(app_info['id'])
        print(f"✓ Found {len(localizations)} localization(s)")
        
        # Create locale to ID mapping
        locale_map = {}
        for loc in localizations:
            locale = loc['attributes']['locale']
            locale_map[locale] = loc['id']
            print(f"  - {locale}: {loc['attributes'].get('name', 'N/A')}")
        
    except Exception as e:
        print(f"✗ Failed to get localizations: {e}")
        return 1
    
    # Upload icons
    print(f"\n{'[DRY RUN] ' if args.dry_run else ''}Uploading localized icons...")
    
    # Determine which locales to process
    if args.locale:
        if args.locale not in locale_map:
            print(f"✗ Locale {args.locale} not found")
            return 1
        locales_to_process = {args.locale: locale_map[args.locale]}
    else:
        locales_to_process = locale_map
    
    # Process each locale
    success_count = 0
    failed_count = 0
    
    for locale, loc_id in locales_to_process.items():
        # Determine icon path
        if locale in LOCALIZED_ICONS:
            icon_path = Path(args.icons_dir) / LOCALIZED_ICONS[locale]
        else:
            # Fallback to default icon
            icon_path = Path(args.icons_dir) / 'icon_default.png'
        
        # Upload the icon
        result = upload_localized_icon(
            client,
            loc_id,
            locale,
            str(icon_path),
            dry_run=args.dry_run
        )
        
        if result:
            success_count += 1
        else:
            failed_count += 1
    
    # Summary
    print(f"\nSummary:")
    print(f"  Success: {success_count}")
    print(f"  Failed: {failed_count}")
    
    return 0 if failed_count == 0 else 1


if __name__ == '__main__':
    sys.exit(main())