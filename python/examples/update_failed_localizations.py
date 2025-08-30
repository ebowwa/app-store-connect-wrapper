#!/usr/bin/env python3
"""Update failed localizations with shorter content."""

import os
from dotenv import load_dotenv
from app_store_connect import Client
from app_store_connect.base import BaseAPI

# Load environment variables
load_dotenv()

def main():
    """Update failed localizations."""
    print("🌙 Updating Failed Localizations")
    print("================================\n")
    
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
    app_infos = client.apps.get_app_infos(app_id)
    app_info_id = app_infos[-1]["id"]
    
    # Update German (de-DE)
    print("🇩🇪 Updating German...")
    try:
        client.localizations.create(
            app_info_id=app_info_id,
            locale="de-DE",
            name="SchlafZyklen",
            subtitle="Schlafzyklus-Rechner",
            privacy_policy_url=None,
            privacy_policy_text=None
        )
        print("   ✅ Created German app info")
    except Exception as e:
        print(f"   ⚠️  {e}")
    
    # Update French (fr-FR)
    print("🇫🇷 Updating French...")
    try:
        client.localizations.create(
            app_info_id=app_info_id,
            locale="fr-FR",
            name="CyclesSommeil",
            subtitle="Cycles de Sommeil",
            privacy_policy_url=None,
            privacy_policy_text=None
        )
        print("   ✅ Created French app info")
    except Exception as e:
        print(f"   ⚠️  {e}")
    
    # Update Korean (ko)
    print("🇰🇷 Updating Korean...")
    try:
        client.localizations.create(
            app_info_id=app_info_id,
            locale="ko",
            name="슬립루프",
            subtitle="수면 주기 계산기",
            privacy_policy_url=None,
            privacy_policy_text=None
        )
        print("   ✅ Created Korean app info")
    except Exception as e:
        print(f"   ⚠️  {e}")
    
    print("\n✨ Done!")

if __name__ == "__main__":
    main()