# App Store Connect Wrapper - Multi-Language Implementation

A comprehensive library for automating App Store Connect operations, available in multiple programming languages. This repository provides equivalent functionality across different languages, allowing developers to choose their preferred implementation while maintaining consistent API design.

## 🚀 Available Implementations

### 🐍 Python Implementation
**Location**: [`python/`](./python/)

The original Python implementation providing full App Store Connect API functionality.

**Features**:
- JWT authentication with .p8 private keys
- Complete App Store Connect API coverage
- Async/await support
- Comprehensive error handling
- Localization management
- Version control and submission
- Media and metadata management

**Quick Start**:
```bash
cd python/
pip install -e .
```

See [Python README](./python/README.md) for detailed documentation.

### 🦀 Rust Implementation  
**Location**: [`rust/`](./rust/)

High-performance Rust implementation with equivalent functionality to the Python version.

**Features**:
- Memory-safe and performant
- Full async/await support with Tokio
- Type-safe API interactions
- Comprehensive error handling
- Zero-cost abstractions
- Same API design as Python version

**Quick Start**:
```bash
cd rust/
cargo build
cargo test
```

See [Rust README](./rust/README.md) for detailed documentation.

## 🎯 Core Functionality

All implementations provide:

- **Authentication**: JWT token generation using App Store Connect API keys
- **App Management**: Create, update, and manage app metadata
- **Localization**: Bulk update app names, descriptions, and metadata across locales
- **Version Control**: Create versions, manage builds, submit for review
- **Media Management**: Upload and manage app screenshots, icons, and other assets
- **Category Management**: Handle app categories and subcategories

## 🏗️ Repository Structure

```
app-store-connect-wrapper/
├── python/                 # Python implementation
│   ├── app_store_connect/  # Python source code
│   ├── examples/           # Python examples
│   ├── README.md          # Python-specific docs
│   └── pyproject.toml     # Python dependencies
├── rust/                  # Rust implementation  
│   ├── src/               # Rust source code
│   ├── examples/          # Rust examples
│   ├── README.md          # Rust-specific docs
│   └── Cargo.toml         # Rust dependencies
└── README.md              # This file
```

## 🔧 Authentication Setup

All implementations use the same authentication approach:

1. **Generate API Key**: Create a new API key in App Store Connect
2. **Download Private Key**: Save the `.p8` file securely
3. **Set Environment Variables**:
   ```bash
   export ASC_KEY_ID="your-key-id"
   export ASC_ISSUER_ID="your-issuer-id" 
   export ASC_PRIVATE_KEY_PATH="/path/to/your/key.p8"
   ```

## 📚 Examples

Each implementation includes equivalent examples:

- **Sync Localizations**: Bulk update app localizations across multiple locales
- **Version Management**: Create and manage app store versions
- **Media Upload**: Upload and organize app screenshots and assets

## 🚧 Future Implementations

This repository is designed to support additional language implementations:

- **JavaScript/TypeScript**: Planned for web and Node.js environments
- **Python v2**: Next-generation Python implementation with enhanced features
- **Additional Languages**: Open to community contributions

## 🤝 Contributing

Contributions are welcome for:
- Bug fixes and improvements to existing implementations
- New language implementations
- Documentation improvements
- Additional examples and use cases

## 📄 License

This project is licensed under the MIT License - see the individual implementation directories for specific license files.

## 🔗 Links

- [App Store Connect API Documentation](https://developer.apple.com/documentation/appstoreconnectapi)
- [Python Implementation](./python/)
- [Rust Implementation](./rust/)

---

Choose your preferred language implementation and start automating your App Store Connect workflows today! 🚀
