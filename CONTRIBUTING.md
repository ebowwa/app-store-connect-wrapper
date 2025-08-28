# Contributing to App Store Connect Wrapper

Thank you for your interest in contributing! We welcome contributions from everyone.

## Getting Started

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR-USERNAME/app-store-connect-wrapper.git
   cd app-store-connect-wrapper
   ```
3. Install dependencies with `uv`:
   ```bash
   uv pip install -e .
   ```

## Development Setup

1. Copy `.env.template` to `.env` and add your App Store Connect credentials for testing
2. Run tests: `uv run test_real.py`

## Adding New API Endpoints

When implementing a new API area (e.g., TestFlight, Screenshots, etc.):

### 1. Create a New Module

Create a new file in `src/app_store_connect/api/` following this template:

```python
"""
[API Area] module for App Store Connect
"""

from typing import Dict, Any, List, Optional
from ..base import BaseAPI


class [APIName]API(BaseAPI):
    """
    Manage [description] in App Store Connect
    """
    
    def get_all(self, parent_id: str) -> List[Dict[str, Any]]:
        """
        Get all [items]
        
        Args:
            parent_id: The parent resource ID
            
        Returns:
            List of [item] data
        """
        response = super().get(f'endpoint/{parent_id}/items')
        return response.get('data', [])
    
    def get(self, item_id: str) -> Dict[str, Any]:
        """
        Get a specific [item]
        
        Args:
            item_id: The [item] ID
            
        Returns:
            [Item] data
        """
        response = super().get(f'items/{item_id}')
        return response['data']
    
    def create(self, **kwargs) -> Dict[str, Any]:
        """
        Create a new [item]
        """
        data = {
            'data': {
                'type': 'items',
                'attributes': kwargs
            }
        }
        response = super().post('items', data=data)
        return response['data']
    
    def update(self, item_id: str, **kwargs) -> Dict[str, Any]:
        """
        Update an [item]
        """
        data = {
            'data': {
                'type': 'items',
                'id': item_id,
                'attributes': kwargs
            }
        }
        response = super().patch(f'items/{item_id}', data=data)
        return response['data']
    
    def delete(self, item_id: str) -> None:
        """
        Delete an [item]
        """
        super().delete(f'items/{item_id}')
```

### 2. Important Guidelines

- **Always use `super().get/post/patch/delete`** instead of `self.get/post/patch/delete` to avoid URL duplication
- Follow the App Store Connect API documentation for correct endpoint paths
- Include comprehensive docstrings with Args and Returns sections
- Handle pagination using the existing `get_all_pages` method in BaseAPI
- Use type hints for all parameters and return values

### 3. Add to Client

Update `src/app_store_connect/client.py` to include your new API:

```python
from .api.your_module import YourAPI

class Client:
    def __init__(self, ...):
        # ... existing code ...
        self.your_api = YourAPI(self._auth)
```

### 4. Update __init__.py

Add your new API to `src/app_store_connect/api/__init__.py`:

```python
from .your_module import YourAPI

__all__ = [
    # ... existing exports ...
    "YourAPI",
]
```

### 5. Write Tests

Create a test file `tests/test_your_module.py` with at least:
- Unit tests with mocked responses
- Integration test in `test_real.py` if you have credentials

### 6. Update Documentation

- Update the README.md with usage examples for your new API
- Update the roadmap issue (#1) to mark your implemented endpoints

## Code Style

- Use clear, descriptive variable names
- Keep functions focused and single-purpose
- Add type hints to all functions
- Follow PEP 8 style guidelines

## Testing

Before submitting a PR:

1. Ensure all tests pass
2. Add tests for any new functionality
3. Test with real API if possible (using your own credentials)

## Submitting a Pull Request

1. Create a new branch for your feature:
   ```bash
   git checkout -b add-testflight-api
   ```

2. Make your changes and commit with clear messages:
   ```bash
   git add .
   git commit -m "Add TestFlight API module with beta groups support"
   ```

3. Push to your fork:
   ```bash
   git push origin add-testflight-api
   ```

4. Open a Pull Request with:
   - Clear description of what you've implemented
   - Reference to issue #1 for API coverage
   - List of endpoints implemented
   - Any limitations or known issues

## Priority APIs to Implement

Based on community needs (see issue #1):

1. **TestFlight Management** - Beta testing workflows
2. **Screenshots/Previews** - App Store media management
3. **Builds** - Build management and uploads
4. **In-App Purchases** - IAP configuration
5. **Customer Reviews** - Review responses

## Questions?

Feel free to ask questions in the issues or discussions. We're here to help!

## License

By contributing, you agree that your contributions will be licensed under the MIT License.