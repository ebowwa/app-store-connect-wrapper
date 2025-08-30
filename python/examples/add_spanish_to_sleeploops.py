#!/usr/bin/env python3
"""Add Spanish localization to SleepLoops app."""

import os
from dotenv import load_dotenv
from app_store_connect import Client

# Load environment variables
load_dotenv()

def main():
    """Add Spanish localization to SleepLoops."""
    print("🌙 SleepLoops Spanish Localization Updater")
    print("==========================================\n")
    
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
    
    # Spanish (Mexico) content
    spanish_content = {
        "name": "SleepLoops: Planea Tu Sueño",
        "subtitle": "Calculadora de Ciclos de Sueño",
        "privacyPolicyUrl": "",
        "privacyPolicyText": None
    }
    
    # Get app infos and update the primary one
    app_infos = client.apps.get_app_infos(app_id)
    if app_infos:
        # Use the most recent app info (usually the last one)
        app_info = app_infos[-1]
        app_info_id = app_info["id"]
        print(f"📝 Updating App Info: {app_info_id}")
        
        # Create Spanish localization for app info (name and subtitle)
        try:
            result = client.localizations.create(
                app_info_id=app_info_id,
                locale="es-ES",  # Spanish (Spain) 
                name=spanish_content["name"],
                subtitle=spanish_content["subtitle"],
                privacy_policy_url=None,
                privacy_policy_text=None
            )
            print("✅ Created Spanish app info localization!")
            print(f"   Name: {spanish_content['name']}")
            print(f"   Subtitle: {spanish_content['subtitle']}")
        except Exception as e:
            print(f"❌ Error creating app info localization: {e}")
    
    print("\n✨ Done!")

if __name__ == "__main__":
    main()