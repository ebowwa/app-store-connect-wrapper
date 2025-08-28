#!/usr/bin/env python3
"""
Example: Sync app localizations from local files to App Store Connect
"""

import sys
import json
from pathlib import Path
from typing import Dict, Any

# Add parent directory to path for development
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from app_store_connect import Client


# Localization mappings
LOCALE_MAPPING = {
    'de.lproj': 'de-DE',
    'en.lproj': 'en-US',
    'es.lproj': 'es-ES',
    'es-MX.lproj': 'es-MX',
    'fr.lproj': 'fr-FR',
    'ja.lproj': 'ja',
    'ko.lproj': 'ko',
    'pt-BR.lproj': 'pt-BR',
    'ru.lproj': 'ru',
    'zh-Hans.lproj': 'zh-Hans',
    'zh-Hant.lproj': 'zh-Hant',
    'ar.lproj': 'ar-SA',
    'hi.lproj': 'hi',
    'it.lproj': 'it'
}

# App names per locale (from InfoPlist.strings)
APP_NAMES = {
    'de-DE': 'SauberBild',
    'en-US': 'CleanShot',
    'es-ES': 'FotoLimpia',
    'es-MX': 'FotoLimpia México',
    'fr-FR': 'PhotoPure',
    'ja': 'クリーンショット',
    'ko': '클린샷',
    'pt-BR': 'FotoLimpa Brasil',
    'ru': 'ЧистыйСнимок',
    'zh-Hans': '净图',
    'zh-Hant': '淨圖',
    'ar-SA': 'صورة نظيفة',
    'hi': 'साफ़ छवि',
    'it': 'Scatto Pulito'
}

# App subtitles per locale
APP_SUBTITLES = {
    'de-DE': 'Entfernen Sie Metadaten sicher',
    'en-US': 'Remove metadata safely',
    'es-ES': 'Elimina metadatos de forma segura',
    'es-MX': 'Elimina metadatos de forma segura',
    'fr-FR': 'Supprimez les métadonnées en toute sécurité',
    'ja': 'メタデータを安全に削除',
    'ko': '메타데이터를 안전하게 제거',
    'pt-BR': 'Remova metadados com segurança',
    'ru': 'Безопасно удаляйте метаданные',
    'zh-Hans': '安全地删除元数据',
    'zh-Hant': '安全地刪除元數據',
    'ar-SA': 'إزالة البيانات الوصفية بأمان',
    'hi': 'मेटाडेटा को सुरक्षित रूप से हटाएं',
    'it': 'Rimuovi i metadati in sicurezza'
}


def sync_localizations(client: Client, app_id: str, dry_run: bool = False):
    """
    Sync localizations to App Store Connect
    
    Args:
        client: App Store Connect client
        app_id: The app ID
        dry_run: If True, only print what would be done
    """
    print(f"{'[DRY RUN] ' if dry_run else ''}Syncing localizations for app {app_id}...")
    
    # Prepare localizations data
    localizations = {}
    for locale, name in APP_NAMES.items():
        localizations[locale] = {
            'name': name,
            'subtitle': APP_SUBTITLES.get(locale, '')
        }
    
    if dry_run:
        print("\nWould update the following localizations:")
        for locale, data in localizations.items():
            print(f"  {locale}:")
            print(f"    Name: {data['name']}")
            print(f"    Subtitle: {data['subtitle']}")
        return
    
    # Get app info
    print("\nFetching app info...")
    app_infos = client.apps.get_app_infos(app_id)
    if not app_infos:
        print("ERROR: No app info found!")
        return
    
    # Find an editable app info
    app_info_id = None
    for app_info in app_infos:
        state = app_info.get('attributes', {}).get('appStoreState')
        print(f"  App info {app_info['id']}: state={state}")
        if state in ['DEVELOPER_REJECTED', 'PREPARE_FOR_SUBMISSION', 'METADATA_REJECTED']:
            app_info_id = app_info['id']
            print(f"  -> Using editable app info: {app_info_id}")
            break
    
    if not app_info_id:
        print("WARNING: No editable app info found. Using first available.")
        app_info_id = app_infos[0]['id']
    
    # Update localizations
    print(f"\nUpdating localizations for app info {app_info_id}...")
    results = client.localizations.bulk_update(app_info_id, localizations)
    
    # Print results
    success_count = 0
    failure_count = 0
    
    for locale, result in results.items():
        if result['success']:
            success_count += 1
            action = result.get('action', 'updated')
            print(f"  ✓ {locale}: {action}")
        else:
            failure_count += 1
            error = result.get('error', 'Unknown error')
            print(f"  ✗ {locale}: {error}")
    
    print(f"\nSummary:")
    print(f"  Success: {success_count}")
    print(f"  Failed: {failure_count}")
    
    return results


def main():
    """Main entry point"""
    import argparse
    from dotenv import load_dotenv
    import os
    
    parser = argparse.ArgumentParser(description='Sync app localizations to App Store Connect')
    parser.add_argument('--app-id', help='App ID (defaults to env var ASC_APP_ID)')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be done without making changes')
    parser.add_argument('--env-file', default='.env', help='Path to .env file')
    
    args = parser.parse_args()
    
    # Load environment variables
    if Path(args.env_file).exists():
        load_dotenv(args.env_file)
    
    # Get app ID
    app_id = args.app_id or os.getenv('ASC_APP_ID')
    if not app_id:
        print("ERROR: App ID not provided. Use --app-id or set ASC_APP_ID in environment.")
        sys.exit(1)
    
    # Create client
    try:
        client = Client.from_env()
    except ValueError as e:
        print(f"ERROR: {e}")
        sys.exit(1)
    
    # Sync localizations
    try:
        sync_localizations(client, app_id, dry_run=args.dry_run)
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()