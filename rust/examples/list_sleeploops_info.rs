use app_store_connect_rust::{Client, AppStoreConnectError, AuthenticationError};
use std::env;

#[tokio::main]
async fn main() -> Result<(), AppStoreConnectError> {
    println!("🌙 SleepLoops App Info Viewer");
    println!("==============================\n");
    
    // Load environment variables from parent directory's .env
    let _ = dotenvy::from_path("../.env");
    
    // Get credentials
    let key_id = env::var("ASC_KEY_ID")
        .map_err(|_| AppStoreConnectError::Authentication(AuthenticationError::new("ASC_KEY_ID not set")))?;
    let issuer_id = env::var("ASC_ISSUER_ID")
        .map_err(|_| AppStoreConnectError::Authentication(AuthenticationError::new("ASC_ISSUER_ID not set")))?;
    let mut private_key_path = env::var("ASC_PRIVATE_KEY_PATH")
        .map_err(|_| AppStoreConnectError::Authentication(AuthenticationError::new("ASC_PRIVATE_KEY_PATH not set")))?;
    
    // If path starts with ./, make it relative to parent directory
    if private_key_path.starts_with("./") {
        private_key_path = format!("../{}", private_key_path.trim_start_matches("./"));
    }
    
    // Initialize client
    let client = Client::new(&key_id, &issuer_id, &private_key_path).await?;
    println!("✅ Client initialized successfully\n");
    
    // SleepLoops bundle ID
    let bundle_id = "com.ebowwa.sleeploops";
    
    // Find the app by bundle ID
    println!("🔍 Looking for SleepLoops app...");
    let app = client.get_app_by_bundle_id(bundle_id).await?;
    
    if let Some(app_data) = app {
        let app_id = app_data.get("id")
            .and_then(|id| id.as_str())
            .ok_or_else(|| AppStoreConnectError::Api { 
                message: "App ID not found".to_string() 
            })?;
        
        println!("✅ Found app ID: {}\n", app_id);
        
        // Get app store versions
        println!("📱 App Store Versions:");
        let versions = client.versions().get_all(app_id).await?;
        for version in &versions {
            if let Some(attrs) = version.get("attributes") {
                let version_string = attrs.get("versionString").and_then(|v| v.as_str()).unwrap_or("Unknown");
                let state = attrs.get("appStoreState").and_then(|s| s.as_str()).unwrap_or("Unknown");
                let platform = attrs.get("platform").and_then(|p| p.as_str()).unwrap_or("Unknown");
                println!("  - Version {} ({}) - State: {}", version_string, platform, state);
                
                // Get version ID for localization
                if let Some(version_id) = version.get("id").and_then(|id| id.as_str()) {
                    println!("    Version ID: {}", version_id);
                }
            }
        }
        
        println!("\n📝 App Infos:");
        let app_infos = client.apps().get_app_infos(app_id).await?;
        for (idx, info) in app_infos.iter().enumerate() {
            if let Some(info_id) = info.get("id").and_then(|id| id.as_str()) {
                println!("  App Info #{}: {}", idx + 1, info_id);
                
                // Check what type this is
                if let Some(type_val) = info.get("type").and_then(|t| t.as_str()) {
                    println!("    Type: {}", type_val);
                }
                
                // Get localizations for this app info
                let localizations = client.localizations().get_all(info_id).await?;
                println!("    Localizations: {} found", localizations.len());
                for loc in &localizations {
                    if let Some(attrs) = loc.get("attributes") {
                        let locale = attrs.get("locale").and_then(|l| l.as_str()).unwrap_or("Unknown");
                        let name = attrs.get("name").and_then(|n| n.as_str()).unwrap_or("No name");
                        println!("      - {} : {}", locale, name);
                    }
                }
            }
        }
        
    } else {
        println!("❌ App with bundle ID '{}' not found", bundle_id);
    }
    
    println!("\n✨ Done!");
    Ok(())
}