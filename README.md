# OpenSSL Development Environment

**Complete Testing Orchestration for DDD 4-Repository Layered Architecture**

This workspace provides a comprehensive development and testing environment for the OpenSSL ecosystem, containing 8 repositories organized across architectural layers.

## 🚀 Quick Start

### Option 1: VSCode/Cursor Workspace
```bash
cd ~/projects/openssl-devenv
code openssl-devenv.code-workspace
```

### Option 2: DevContainer
```bash
# Open in VSCode/Cursor with devcontainer support
# Automatically sets up full environment
```

### Option 3: Manual Setup
```bash
# Configure environment
cp .env.example .env  # Edit with your CLOUDSMITH_API_KEY

# Setup Conan user/channel (optional)
./scripts/setup-conan-env.sh

# Run setup
./scripts/setup-dev-env.sh

# Run tests
./scripts/run-integration-tests.sh
```

## 📦 Conan Package Management

This environment uses Conan for C/C++ package management with user/channel support for organizing package versions across different environments.

### Version Compatibility Matrix

| Repository | Version | Channel | Dependencies | Purpose |
|------------|---------|---------|--------------|---------|
| **openssl-conan-base** | 1.0.1 | stable | None | Foundation utilities, profiles, Python runtime |
| **openssl-fips-policy** | 140-3.2 | stable | None | FIPS 140-3 certificates and compliance data |
| **openssl-tools** | 1.2.4 | stable | openssl-base/1.0.1+ | Build orchestration and tooling |
| **openssl** | 4.0.0-dev | stable | openssl-tools/1.2.4+, openssl-fips-data/140-3.2+ | Core cryptographic library |

### Dynamic Version Management

The OpenSSL repository uses dynamic version reading from `VERSION.dat`:

```python
def set_version(self):
    """Read version from VERSION.dat file"""
    version_file = os.path.join(self.recipe_folder, "VERSION.dat")
    if os.path.exists(version_file):
        # Parse MAJOR, MINOR, PATCH, PRE_RELEASE_TAG
        # Build semantic version: 4.0.0-dev
        self.version = parsed_version
```

### User/Channel Configuration

```bash
# Setup environment variables
export CONAN_USER=sparesparrow
export CONAN_CHANNEL=stable  # or dev, testing, etc.

# Or use the setup script
./scripts/setup-conan-env.sh
```

### Package References

Packages are referenced with user/channel format:
```
openssl/3.4.1@sparesparrow/stable
openssl-build-tools/1.2.0@sparesparrow/dev
openssl-base/1.0.0@sparesparrow/stable
```

### Available Channels

- **`stable`**: Production-ready releases
- **`dev`**: Development builds with latest features
- **`testing`**: Pre-release testing builds

### Consumer Usage

```bash
# Install stable packages
conan install openssl/3.4.1@sparesparrow/stable

# Or use environment variables
conan install openssl/3.4.1@${CONAN_USER}/${CONAN_CHANNEL}
```

## 🏗️ Architecture Layers

### 🔐 Foundation Layer
- **openssl-conan-base**: Utilities, SBOM generation, profiles
- **openssl-fips-policy**: FIPS certificates and compliance data

### 🛠️ Tooling Layer
- **openssl-tools**: Build orchestration consuming foundation

### 🔬 Testing & Integration
- **fuzz-corpora**: Test data for fuzzing
- **libcurl**: HTTP integration testing
- **openssl-docs**: Documentation

### 🌐 Domain Layer
- **openssl**: Core cryptographic library

### 🤖 Orchestration Layer
- **mcp-project-orchestrator**: AI templates and Cursor integration

## 🧪 Testing Scenarios

Run comprehensive integration tests:
```bash
./scripts/run-integration-tests.sh
```

### Individual Test Categories

**Dependency Management**:
```bash
cd openssl-tools && conan create . --build=missing
```

**Python Automation**:
```bash
cd openssl-conan-base && pytest tests/
```

**Cloudsmith Integration**:
```bash
conan search "*" -r=${CONAN_REPOSITORY_NAME}
```

**Developer Workflow**:
```bash
cd mcp-project-orchestrator
source venv/bin/activate
mcp-orchestrator create-openssl-project --project-name test-app
```

## 📊 Expected Behaviors

### Foundation Layer
- **openssl-conan-base**: Self-contained utilities with comprehensive tests
- **openssl-fips-policy**: Static certificate data, integrity verified

### Tooling Layer
- **openssl-tools**: Fast builds, consumes foundation from Cloudsmith

### Domain Layer
- **openssl**: 5-phase aerospace build process, multi-target support

### Orchestration Layer
- **mcp-project-orchestrator**: AI-enhanced project creation and IDE integration

## 🔧 Configuration

Edit `.env` file:
```bash
CLOUDSMITH_API_KEY=your-api-key-here
# ... other configuration
```

## 🎯 Success Criteria

- ✅ All 8 repositories functional
- ✅ Cross-layer dependencies resolve
- ✅ CI/CD publishes to Cloudsmith
- ✅ AI integration working
- ✅ Performance benchmarks met

## 📚 Documentation

See `CLAUDE.md` for comprehensive testing guidelines and component behaviors.
