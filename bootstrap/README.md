# OpenSSL Conan Bootstrap Script

One-command setup for the sparesparrow OpenSSL development environment.

## Quick Start

### One-Line Installation

```bash
# Development mode (recommended)
curl -sSL https://raw.githubusercontent.com/sparesparrow/openssl-devenv/main/bootstrap/openssl-conan-init.py | python3 - --dev

# Minimal mode (Conan only)
curl -sSL https://raw.githubusercontent.com/sparesparrow/openssl-devenv/main/bootstrap/openssl-conan-init.py | python3 - --minimal
```

### Clone and Run

```bash
git clone https://github.com/sparesparrow/openssl-devenv.git
cd openssl-devenv/bootstrap
python3 openssl-conan-init.py --dev
```

## Installation Modes

| Mode | Duration | What's Included | Use Case |
|------|----------|-----------------|----------|
| `--minimal` | 2-3 minutes | Conan 2.21.0 + remotes + profile | Quick Conan setup |
| `--full` | 8-12 minutes | Minimal + repos + extensions | Full development |
| `--dev` | 12-15 minutes | Full + VS Code config | Complete IDE setup |

### Mode Details

#### Minimal Mode (`--minimal`)
- ✅ Install Conan 2.21.0 (pinned version)
- ✅ Configure remotes (sparesparrow-conan, conancenter)
- ✅ Detect Conan profile
- ✅ Verify installation

#### Full Mode (`--full`)
- ✅ Everything in minimal mode
- ✅ Clone all repositories to `~/sparesparrow/`
- ✅ Install Conan extensions
- ✅ Set up development environment

#### Development Mode (`--dev`)
- ✅ Everything in full mode
- ✅ VS Code workspace configuration
- ✅ IntelliSense setup
- ✅ Debug configurations
- ✅ Recommended extensions

## Options

### `--dry-run`
Show what would be done without making changes:
```bash
python3 openssl-conan-init.py --dev --dry-run
```

### `--test-mode`
Run in test mode for CI validation:
```bash
python3 openssl-conan-init.py --minimal --test-mode
```

### `--validate`
Validate existing installation:
```bash
python3 openssl-conan-init.py --validate
```

## What Gets Installed

### Conan Configuration
- **Version**: 2.21.0 (pinned)
- **Remotes**: 
  - `sparesparrow-conan`: https://cloudsmith.io/~sparesparrow-conan/repos/openssl-conan/
  - `conancenter`: https://center.conan.io
- **Profile**: Auto-detected for your platform

### Repositories (Full/Dev modes)
Cloned to `~/sparesparrow/`:
- `openssl/` - OpenSSL source with Conan integration
- `openssl-tools/` - Conan extensions and reusable workflows
- `openssl-conan-base/` - Production profiles and CI/CD
- `openssl-fips-policy/` - FIPS 140-3 compliance
- `openssl-devenv/` - This development environment

### Extensions (Full/Dev modes)
Installed to `~/.conan2/extensions/`:
- `conan openssl:build` - Simplified OpenSSL build command
- `conan openssl:graph` - Dependency analysis
- `full_deploy_enhanced` - Enhanced deployment with SBOM

### VS Code Configuration (Dev mode)
Created in `.vscode/`:
- `extensions.json` - Recommended extensions
- `settings.json` - Workspace settings
- `launch.json` - Debug configurations

## Platform Support

| Platform | Status | Notes |
|----------|--------|-------|
| **Ubuntu 22.04+** | ✅ Fully supported | Primary development platform |
| **macOS 13+** | ✅ Fully supported | Intel and Apple Silicon |
| **Windows 11 WSL2** | ✅ Supported | Ubuntu on WSL recommended |
| **Windows 11 Native** | ⚠️ Experimental | PowerShell support limited |

## After Installation

### Quick Commands
```bash
# Navigate to OpenSSL
cd ~/sparesparrow/openssl

# Use custom commands
conan openssl:build --help
conan openssl:graph --json

# Open in VS Code (dev mode)
code .
```

### Verify Installation
```bash
# Check Conan version
conan --version

# List remotes
conan remote list

# Test custom commands
conan openssl:build --help
```

## Troubleshooting

### Common Issues

**Q: "Python 3.8+ is required"**
```bash
# Check Python version
python3 --version

# Install Python 3.8+ if needed
sudo apt update && sudo apt install python3.8  # Ubuntu
brew install python@3.11  # macOS
```

**Q: "Failed to install Conan"**
```bash
# Update pip
python3 -m pip install --upgrade pip

# Try with user install
python3 -m pip install --user conan==2.21.0
```

**Q: "Git clone failed"**
```bash
# Check git installation
git --version

# Install git if needed
sudo apt install git  # Ubuntu
brew install git      # macOS
```

**Q: "Extensions not found"**
```bash
# Check extensions directory
ls ~/.conan2/extensions/

# Re-run with --full mode
python3 openssl-conan-init.py --full
```

### Validation

Run validation to check your installation:
```bash
python3 openssl-conan-init.py --validate
```

### Reset Installation

To start fresh:
```bash
# Remove Conan configuration
rm -rf ~/.conan2

# Remove repositories
rm -rf ~/sparesparrow

# Remove VS Code config
rm -rf .vscode

# Re-run bootstrap
python3 openssl-conan-init.py --dev
```

## Performance

### Expected Times
- **Minimal**: 2-3 minutes
- **Full**: 8-12 minutes  
- **Dev**: 12-15 minutes

### Success Criteria
- ✅ All modes complete in <15 minutes
- ✅ Idempotent (can run multiple times safely)
- ✅ Cross-platform compatibility
- ✅ Offline repository cloning

## Security

- **Pinned versions**: Conan 2.21.0 for reproducibility
- **Verified sources**: All repositories from sparesparrow organization
- **No credentials**: No API keys or secrets required
- **Local installation**: Everything installed locally

## Support

- **Issues**: [GitHub Issues](https://github.com/sparesparrow/openssl-devenv/issues)
- **Documentation**: [Getting Started Guide](../docs/getting-started.md)
- **Community**: [Discussions](https://github.com/sparesparrow/openssl-devenv/discussions)

## License

Apache-2.0 (same as OpenSSL)
