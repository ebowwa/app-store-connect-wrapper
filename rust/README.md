# App Store Connect Rust API Wrapper

A comprehensive Rust wrapper for automating App Store Connect operations, including app metadata management, localization updates, and version control.

## Features

- 🔐 **JWT Authentication**: Secure authentication using App Store Connect API keys
- 🌍 **Localization Management**: Bulk update app names, subtitles, and descriptions across all locales
- 📱 **App Management**: Retrieve and update app information
- 🚀 **Version Control**: Create and manage app store versions
- 🎯 **Smart State Detection**: Automatically finds editable app states for updates
- ⚡ **Bulk Operations**: Efficiently update multiple localizations in a single operation
- 🔄 **Pagination Support**: Handle large datasets with automatic pagination
- 🦀 **Async/Await**: Built with modern Rust async patterns for performance
- 🛡️ **Type Safety**: Leverages Rust's type system for compile-time safety

## Installation

Add this to your `Cargo.toml`:

```toml
[dependencies]
app-store-connect-rust = "0.1.0"
tokio = { version = "1.0", features = ["full"] }
```

## Quick Start

### 1. Set up your credentials

Create a `.env` file:

```env
ASC_KEY_ID=YOUR_KEY_ID
ASC_ISSUER_ID=YOUR_ISSUER_ID
ASC_PRIVATE_KEY_PATH=./AuthKey_YOUR_KEY_ID.p8
ASC_APP_ID=YOUR_APP_ID
```

### 2. Basic usage

```rust
use app_store_connect_rust::Client;
use std::collections::HashMap;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Create client from environment variables
    let client = Client::from_env().await?;

    // Get all your apps
    let apps = client.apps().get_all(None).await?;
    for app in apps {
        if let (Some(name), Some(bundle_id)) = (
            app.get("attributes").and_then(|a| a.get("name")).and_then(|n| n.as_str()),
            app.get("attributes").and_then(|a| a.get("bundleId")).and_then(|b| b.as_str())
        ) {
            println!("App: {} ({})", name, bundle_id);
        }
    }

    // Get app by bundle ID
    if let Some(app) = client.get_app_by_bundle_id("com.example.app").await? {
        println!("Found app: {:?}", app);
    }

    // Update app localizations
    let mut localizations = HashMap::new();
    localizations.insert("en-US".to_string(), serde_json::json!({
        "name": "My App",
        "subtitle": "Amazing App"
    }));
    localizations.insert("fr-FR".to_string(), serde_json::json!({
        "name": "Mon App", 
        "subtitle": "App Incroyable"
    }));
    localizations.insert("es-ES".to_string(), serde_json::json!({
        "name": "Mi App",
        "subtitle": "App Increíble"
    }));

    let app_id = "your_app_id";
    let results = client.update_app_localizations(app_id, localizations).await?;
    
    for (locale, result) in results {
        println!("Locale {}: {:?}", locale, result);
    }

    Ok(())
}
```

## API Modules

### Apps API

```rust
// Get all apps
let apps = client.apps().get_all(None).await?;

// Get specific app
let app = client.apps().get("app_id").await?;

// Get app by bundle ID
let app = client.apps().get_by_bundle_id("com.example.app").await?;

// Update app attributes
let attributes = serde_json::json!({"primaryLocale": "en-US"});
let updated = client.apps().update("app_id", attributes).await?;

// Get app infos
let app_infos = client.apps().get_app_infos("app_id").await?;

// Get app store versions
let versions = client.apps().get_app_store_versions("app_id").await?;
```

### Localizations API

```rust
// Get all localizations for an app info
let localizations = client.localizations().get_all("app_info_id").await?;

// Get specific localization
let loc = client.localizations().get("localization_id").await?;

// Create new localization
let new_loc = client.localizations().create(
    "app_info_id",
    "fr-FR",
    Some("Mon App"),
    Some("Une super app"),
    None,
    None
).await?;

// Update localization
let updated = client.localizations().update(
    "localization_id",
    Some("Updated Name"),
    Some("Updated Subtitle"),
    None,
    None
).await?;

// Bulk update localizations
let mut localizations = HashMap::new();
localizations.insert("en-US".to_string(), serde_json::json!({
    "name": "My App",
    "subtitle": "Great App"
}));
localizations.insert("fr-FR".to_string(), serde_json::json!({
    "name": "Mon App",
    "subtitle": "Super App"
}));

let results = client.localizations().bulk_update("app_info_id", localizations).await?;
```

### Versions API

```rust
// Get all versions
let versions = client.versions().get_all("app_id").await?;

// Get current version
let current = client.versions().get_current("app_id").await?;

// Create new version
let new_version = client.versions().create(
    "app_id",
    "1.0.1",
    Some("IOS"),
    Some("© 2024 My Company"),
    Some("MANUAL")
).await?;

// Update version
let updated = client.versions().update(
    "version_id",
    Some("1.0.2"),
    Some("© 2024 My Company"),
    Some("AFTER_APPROVAL"),
    None,
    None,
    None,
    None
).await?;

// Submit for review
let submission = client.versions().submit_for_review("version_id").await?;
```

## Examples

### Sync Localizations from Local Data

```bash
# Run the sync script
cargo run --example sync_localizations

# Dry run to see what would be updated
cargo run --example sync_localizations -- --dry-run
```

### Update App Metadata Programmatically

```rust
use app_store_connect_rust::Client;
use std::collections::HashMap;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let client = Client::from_env().await?;

    // Prepare localizations
    let mut localizations = HashMap::new();
    localizations.insert("en-US".to_string(), serde_json::json!({
        "name": "My App",
        "subtitle": "Amazing App"
    }));
    localizations.insert("fr-FR".to_string(), serde_json::json!({
        "name": "Mon App",
        "subtitle": "App Incroyable"
    }));

    // Update all localizations
    let app_id = "YOUR_APP_ID";
    let results = client.update_app_localizations(app_id, localizations).await?;

    // Check results
    for (locale, result) in results {
        if let Some(success) = result.get("success").and_then(|s| s.as_bool()) {
            if success {
                let action = result.get("action").and_then(|a| a.as_str()).unwrap_or("updated");
                println!("✓ {}: {}", locale, action);
            } else {
                let error = result.get("error").and_then(|e| e.as_str()).unwrap_or("Unknown error");
                println!("✗ {}: {}", locale, error);
            }
        }
    }

    Ok(())
}
```

## Error Handling

```rust
use app_store_connect_rust::{Client, AppStoreConnectError, ValidationError};

#[tokio::main]
async fn main() {
    let client = Client::from_env().await.unwrap();

    match client.localizations().update("loc_id", Some("New Name"), None, None, None).await {
        Ok(result) => println!("Success: {:?}", result),
        Err(AppStoreConnectError::Validation(e)) => {
            println!("Validation failed: {}", e);
        }
        Err(e) => {
            println!("API error: {}", e);
        }
    }
}
```

## Important Notes

### App State Requirements

The App Store Connect API requires apps to be in specific states to allow updates:

- ✅ **Editable states**: `DEVELOPER_REJECTED`, `PREPARE_FOR_SUBMISSION`, `METADATA_REJECTED`
- ❌ **Read-only states**: `READY_FOR_SALE`, `IN_REVIEW`, `WAITING_FOR_REVIEW`

The wrapper automatically detects and uses editable app info records when available.

### Rate Limiting

The App Store Connect API has rate limits. The wrapper includes:
- Automatic retry logic for rate limit errors
- Proper error handling with descriptive messages
- Token refresh before expiration

### Localization Codes

Use standard locale codes for localizations:
- `en-US` - English (United States)
- `de-DE` - German
- `fr-FR` - French
- `es-ES` - Spanish (Spain)
- `es-MX` - Spanish (Mexico)
- `ja` - Japanese
- `zh-Hans` - Chinese (Simplified)
- `zh-Hant` - Chinese (Traditional)
- etc.

## Development

### Running Tests

```bash
# Run all tests
cargo test

# Run with output
cargo test -- --nocapture

# Run specific test
cargo test test_auth
```

### Building

```bash
# Build the library
cargo build

# Build with optimizations
cargo build --release

# Check for errors without building
cargo check
```

### Linting and Formatting

```bash
# Format code
cargo fmt

# Run clippy for linting
cargo clippy

# Run clippy with all features
cargo clippy --all-features
```

## License

MIT License - See LICENSE file for details

## Comparison with Python Version

This Rust implementation provides equivalent functionality to the Python version with these advantages:

- **Performance**: Async/await with zero-cost abstractions
- **Safety**: Compile-time guarantees against null pointer exceptions and data races
- **Memory Management**: Automatic memory management without garbage collection
- **Type Safety**: Strong typing prevents many runtime errors
- **Concurrency**: Built-in support for safe concurrent operations

The API surface is designed to be familiar to users of the Python version while leveraging Rust's strengths.
