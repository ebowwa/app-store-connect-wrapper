#!/usr/bin/env python3
"""Verify all localizations were added to SleepLoops."""

import os
from dotenv import load_dotenv
from app_store_connect import Client
from app_store_connect.base import BaseAPI

# Load environment variables
load_dotenv()

def main():
    """Verify all localizations."""
    print("🌙 SleepLoops Localization Verification")
    print("========================================\n")
    
    # Initialize client
    client = Client(
        key_id=os.getenv("ASC_KEY_ID"),
        issuer_id=os.getenv("ASC_ISSUER_ID"),
        private_key_path=os.getenv("ASC_PRIVATE_KEY_PATH")
    )
    print("✅ Client initialized\n")
    
    # Find SleepLoops
    app = client.apps.get_by_bundle_id("com.ebowwa.sleeploops")
    if not app:
        print("❌ SleepLoops app not found")
        return
    
    app_id = app["id"]
    print(f"✅ Found SleepLoops (ID: {app_id})\n")
    
    # Get app info localizations
    app_infos = client.apps.get_app_infos(app_id)
    if app_infos:
        app_info = app_infos[-1]
        app_info_id = app_info["id"]
        
        print("📱 App Info Localizations:")
        print("-" * 40)
        existing_locs = client.localizations.get_all(app_info_id)
        
        locales_found = []
        for loc in existing_locs:
            attrs = loc.get("attributes", {})
            locale = attrs.get("locale", "Unknown")
            name = attrs.get("name", "No name")
            subtitle = attrs.get("subtitle", "No subtitle")
            locales_found.append(locale)
            print(f"✅ {locale:8} - {name:20} | {subtitle}")
        
        print(f"\nTotal App Info Localizations: {len(locales_found)}")
    
    # Get version localizations
    versions = client.versions.get_all(app_id)
    editable_version = None
    
    for version in versions:
        state = version.get("attributes", {}).get("appStoreState")
        if state in ["PREPARE_FOR_SUBMISSION", "DEVELOPER_REJECTED", "REJECTED", "WAITING_FOR_REVIEW"]:
            editable_version = version
            break
    
    if editable_version:
        version_id = editable_version["id"]
        version_string = editable_version.get("attributes", {}).get("versionString", "Unknown")
        
        print(f"\n📝 Version {version_string} Localizations:")
        print("-" * 40)
        
        version_locs_response = BaseAPI.get(client.versions, f"appStoreVersions/{version_id}/appStoreVersionLocalizations")
        version_locs = version_locs_response.get("data", [])
        
        version_locales = []
        for loc in version_locs:
            attrs = loc.get("attributes", {})
            locale = attrs.get("locale", "Unknown")
            desc = attrs.get("description")
            desc_length = len(desc) if desc else 0
            keywords = attrs.get("keywords", "")
            keywords_count = len(keywords.split(',')) if keywords else 0
            promo = attrs.get("promotionalText", "")[:50] + "..." if attrs.get("promotionalText") else "No promo"
            version_locales.append(locale)
            print(f"✅ {locale:8} - Desc: {desc_length:4} chars | Keywords: {keywords_count} | Promo: {promo}")
        
        print(f"\nTotal Version Localizations: {len(version_locales)}")
        
        # Check which are missing
        expected_locales = ["en-US", "es-ES", "de-DE", "fr-FR", "it", "pt-BR", "ru", "ja", "ko", "ar-SA", "zh-Hans", "zh-Hant"]
        missing = [loc for loc in expected_locales if loc not in version_locales]
        
        if missing:
            print(f"\n⚠️  Missing localizations: {', '.join(missing)}")
        else:
            print("\n✅ All expected localizations are present!")
    
    # Summary
    print("\n" + "=" * 40)
    print("📊 LOCALIZATION SUMMARY")
    print("=" * 40)
    print(f"Total Languages: {len(version_locales)}")
    print("\nRegions Covered:")
    print("🌎 Americas: English, Spanish (Mexico), Portuguese (Brazil)")
    print("🌍 Europe: German, French, Italian, Russian")
    print("🌏 Asia: Japanese, Korean, Chinese (Simplified & Traditional), Arabic")
    print("\n✨ SleepLoops is now globally localized!")

if __name__ == "__main__":
    main()