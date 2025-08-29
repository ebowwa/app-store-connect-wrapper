#!/usr/bin/env python3
"""Test script to verify App Store Connect API connection."""

import os
from dotenv import load_dotenv
from python.app_store_connect import Client

# Load environment variables
load_dotenv()

def test_connection():
    """Test the App Store Connect API connection."""
    try:
        # Initialize the client
        client = Client(
            key_id=os.getenv("ASC_KEY_ID"),
            issuer_id=os.getenv("ASC_ISSUER_ID"),
            private_key_path=os.getenv("ASC_PRIVATE_KEY_PATH")
        )
        
        print("✅ Client initialized successfully")
        
        # Try to fetch apps (this will validate the authentication)
        apps = client.apps.get_all()
        print(f"✅ Successfully connected! Found {len(apps)} apps")
        
        # Show app details if any exist
        if apps:
            for app in apps[:3]:  # Show first 3 apps
                print(f"  - {app.get('attributes', {}).get('name', 'Unknown')} ({app.get('attributes', {}).get('bundleId', 'Unknown')})")
        
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

if __name__ == "__main__":
    test_connection()