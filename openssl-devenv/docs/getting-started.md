# Getting Started - sparesparrow OpenSSL Development

## Quick Start (5 minutes)

### 1. Bootstrap

```
curl -sSL https://raw.githubusercontent.com/sparesparrow/openssl-devenv/main/bootstrap/openssl-conan-init.py | python3 - --dev
```

### 2. Build OpenSSL

```
# Standard build
conan openssl:build

# With FIPS
conan openssl:build --fips --profile=linux-gcc11-fips
```

### 3. Verify

```
cd ~/sparesparrow/openssl
conan openssl:graph --json
```

## Architecture Overview

```
sparesparrow/
├── openssl-tools/          # Python_requires + extensions
├── openssl-conan-base/     # Profiles + CI/CD
├── openssl/                # Minimal fork for testing
├── openssl-fips-policy/    # FIPS configuration
└── openssl-devenv/         # Developer workspace (you are here)
```

## Common Tasks

### Build for different platforms

```
# Linux with GCC 11
conan openssl:build --profile=linux-gcc11-fips

# Windows with MSVC 19.3
conan openssl:build --profile=windows-msvc193

# macOS ARM64
conan openssl:build --profile=macos-arm64
```

### Enable editable mode

```
cd ~/sparesparrow/openssl-tools
conan editable add . openssl-tools/1.2.0

# Now changes in openssl-tools immediately affect builds
conan openssl:build
```

### Debug build issues

```
# Verbose output
conan openssl:build -vv

# Keep build folder
conan openssl:build --keep-build-folder

# Inspect graph
conan openssl:graph --json | jq .
```

## IDE Setup

### VS Code

1. **Install extensions** (automatic on first open)
2. **Update IntelliSense**:
   ```
   cd openssl
   mkdir build && cd build
   conan install .. --build=missing
   python ../scripts/update-intellisense.py
   ```
3. **Start debugging**: F5 or Run → Start Debugging

### CLion

Add Conan profile to CMake settings:
```
-DCMAKE_TOOLCHAIN_FILE=build/conan_toolchain.cmake
```

## Troubleshooting

### "Conan command not found"

```
python3 -m pip install --user conan>=2.0
export PATH="$HOME/.local/bin:$PATH"
```

### "FIPS self-test failed"

Check module hash:
```
openssl dgst -sha256 -provider fips /usr/local/lib/ossl-modules/fips.so
```

Compare with expected hash in `openssl-fips-policy/fips/expected_module_hash.txt`

### IntelliSense not working

```
cd openssl
python scripts/update-intellisense.py
```

Reload VS Code window (Cmd/Ctrl + Shift + P → "Developer: Reload Window")

## Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) for:
- Code style guidelines
- PR process
- Testing requirements
