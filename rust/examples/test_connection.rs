use app_store_connect_rust::{Client, AppStoreConnectError, AuthenticationError};
use std::env;

#[tokio::main]
async fn main() -> Result<(), AppStoreConnectError> {
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
    println!("✅ Client initialized successfully");
    
    // Try to fetch apps
    match client.apps().get_all(Some(10)).await {
        Ok(apps) => {
            println!("✅ Successfully connected! Found {} apps", apps.len());
            
            // Show first 3 apps
            for app in apps.iter().take(3) {
                if let Some(attrs) = app.get("attributes") {
                    let name = attrs.get("name")
                        .and_then(|n| n.as_str())
                        .unwrap_or("Unknown");
                    let bundle_id = attrs.get("bundleId")
                        .and_then(|b| b.as_str())
                        .unwrap_or("Unknown");
                    println!("  - {} ({})", name, bundle_id);
                }
            }
        }
        Err(e) => {
            println!("❌ Connection failed: {}", e);
        }
    }
    
    Ok(())
}