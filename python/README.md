# App Store Connect API Wrapper

A comprehensive Python wrapper for automating App Store Connect operations, including app metadata management, localization updates, and version control.

## Features

- 🔐 **JWT Authentication**: Secure authentication using App Store Connect API keys
- 🌍 **Localization Management**: Bulk update app names, subtitles, and descriptions across all locales
- 📱 **App Management**: Retrieve and update app information
- 🚀 **Version Control**: Create and manage app store versions
- 🎯 **Smart State Detection**: Automatically finds editable app states for updates
- ⚡ **Bulk Operations**: Efficiently update multiple localizations in a single operation
- 🔄 **Pagination Support**: Handle large datasets with automatic pagination

## Installation

```bash
# Install with pip
pip install -e .

# Or with uv
uv pip install -e .
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

```python
from app_store_connect import Client

# Create client from environment variables
client = Client.from_env()

# Get all your apps
apps = client.apps.get_all()
for app in apps:
    print(f"App: {app['attributes']['name']} ({app['attributes']['bundleId']})")

# Get app by bundle ID
app = client.get_app_by_bundle_id('com.example.app')

# Update app localizations
localizations = {
    'en-US': {'name': 'My App', 'subtitle': 'Amazing App'},
    'fr-FR': {'name': 'Mon App', 'subtitle': 'App Incroyable'},
    'es-ES': {'name': 'Mi App', 'subtitle': 'App Increíble'}
}
results = client.update_app_localizations(app['id'], localizations)
```

## API Modules

### Apps API

```python
# Get all apps
apps = client.apps.get_all()

# Get specific app
app = client.apps.get(app_id)

# Get app by bundle ID
app = client.apps.get_by_bundle_id('com.example.app')

# Update app attributes
updated = client.apps.update(app_id, primaryLocale='en-US')

# Get app infos
app_infos = client.apps.get_app_infos(app_id)

# Get app store versions
versions = client.apps.get_app_store_versions(app_id)
```

### Localizations API

```python
# Get all localizations for an app info
localizations = client.localizations.get_all(app_info_id)

# Get specific localization
loc = client.localizations.get(localization_id)

# Create new localization
new_loc = client.localizations.create(
    app_info_id,
    locale='fr-FR',
    name='Mon App',
    subtitle='Une super app'
)

# Update localization
updated = client.localizations.update(
    localization_id,
    name='Updated Name',
    subtitle='Updated Subtitle'
)

# Bulk update localizations
results = client.localizations.bulk_update(app_info_id, {
    'en-US': {'name': 'My App', 'subtitle': 'Great App'},
    'fr-FR': {'name': 'Mon App', 'subtitle': 'Super App'}
})
```

### Versions API

```python
# Get all versions
versions = client.versions.get_all(app_id)

# Get current version
current = client.versions.get_current(app_id)

# Create new version
new_version = client.versions.create(
    app_id,
    version_string='1.0.1',
    release_type='MANUAL'
)

# Update version
updated = client.versions.update(
    version_id,
    copyright='© 2024 My Company',
    release_type='AFTER_APPROVAL'
)

# Submit for review
submission = client.versions.submit_for_review(version_id)
```

## Examples

### Sync Localizations from Local Files

```bash
# Run the sync script
python examples/sync_localizations.py --app-id YOUR_APP_ID

# Dry run to see what would be updated
python examples/sync_localizations.py --app-id YOUR_APP_ID --dry-run
```

### Update App Metadata Programmatically

```python
from app_store_connect import Client
import json

client = Client.from_env()

# Load localizations from JSON
with open('localizations.json') as f:
    localizations = json.load(f)

# Update all localizations
app_id = 'YOUR_APP_ID'
results = client.update_app_localizations(app_id, localizations)

# Check results
for locale, result in results.items():
    if result['success']:
        print(f"✓ {locale}: {result['action']}")
    else:
        print(f"✗ {locale}: {result['error']}")
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

## Error Handling

```python
from app_store_connect import Client, AppStoreConnectError, ValidationError

client = Client.from_env()

try:
    # Attempt to update localization
    result = client.localizations.update(loc_id, name='New Name')
except ValidationError as e:
    print(f"Validation failed: {e}")
except AppStoreConnectError as e:
    print(f"API error: {e}")
```

## Development

### Project Structure

```
app-store-connect-wrapper/
├── src/
│   └── app_store_connect/
│       ├── __init__.py
│       ├── client.py           # Main client class
│       ├── auth.py             # JWT authentication
│       ├── base.py             # Base API class
│       ├── exceptions.py       # Custom exceptions
│       └── api/
│           ├── __init__.py
│           ├── apps.py         # Apps API
│           ├── localizations.py # Localizations API
│           └── versions.py     # Versions API
├── examples/
│   └── sync_localizations.py   # Example sync script
├── tests/                       # Unit tests
├── pyproject.toml              # Package configuration
└── README.md                   # This file
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app_store_connect

# Run specific test
pytest tests/test_auth.py
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

MIT License - See LICENSE file for details

## Support

For issues and questions:
- Open an issue on GitHub
- Check existing issues for solutions
- Provide detailed error messages and context

## Roadmap

- [ ] Add builds management
- [ ] Implement screenshots and app previews upload
- [ ] Add review responses management
- [ ] Implement TestFlight management
- [ ] Add analytics data retrieval
- [ ] Create CLI tool
- [ ] Add async/await support
- [ ] Implement webhook support