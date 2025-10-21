# Verification Scripts Documentation

This document describes the verification scripts for the OpenSSL Conan development environment.

## Overview

The verification suite consists of three main scripts that test different aspects of the bootstrap and development environment:

1. **`verify-bootstrap.sh`** - Tests the bootstrap script functionality
2. **`verify-commands.py`** - Tests custom Conan commands
3. **`verify-deployer.sh`** - Tests the enhanced deployer functionality

## Scripts

### verify-bootstrap.sh

**Purpose**: Verify the bootstrap script (`openssl-conan-init.py`) works correctly.

**Location**: `scripts/verify-bootstrap.sh`

**Tests**:
- Bootstrap script exists and is executable
- Bootstrap script syntax validation
- Bootstrap script help output
- Dry run mode functionality
- Test mode functionality
- Fresh installation test (minimal mode)
- Remote configuration test
- Idempotency test (running twice should succeed)
- Full mode dry run test
- Dev mode dry run test
- Validation mode test
- Error handling test

**Usage**:
```bash
# Run all bootstrap verification tests
./scripts/verify-bootstrap.sh

# Make executable if needed
chmod +x scripts/verify-bootstrap.sh
```

**Expected Output**:
```
[INFO] Starting bootstrap script verification
[PASS] Bootstrap script exists and is executable
[PASS] Bootstrap script syntax is valid
[PASS] Bootstrap script help command works
...
[PASS] All tests passed!
```

### verify-commands.py

**Purpose**: Verify custom Conan commands are installed and working.

**Location**: `scripts/verify-commands.py`

**Tests**:
- Conan installation check
- Command visibility in `conan --help`
- `conan openssl:build --help` functionality
- `conan openssl:graph --help` functionality
- Graph analyzer with test conanfile
- Command error handling

**Usage**:
```bash
# Run all command verification tests
python3 scripts/verify-commands.py

# With custom Conan path
python3 scripts/verify-commands.py --conan-path /usr/local/bin/conan
```

**Expected Output**:
```
🔧 Checking Conan installation
✅ Conan 2.21.0 is installed and accessible
🔧 Checking command visibility in conan --help
✅ OpenSSL commands visible in conan --help
...
✅ All tests passed!
```

### verify-deployer.sh

**Purpose**: Verify the enhanced deployer functionality.

**Location**: `scripts/verify-deployer.sh`

**Tests**:
- Conan availability check
- Enhanced deployer availability
- Test conanfile creation
- Deployer execution
- Deploy folder structure verification
- SBOM generation (CycloneDX format)
- Metadata generation
- Cache path mapping
- Symlink strategy (if OPENSSL_DEVENV is set)
- Error handling
- Performance test

**Usage**:
```bash
# Run all deployer verification tests
./scripts/verify-deployer.sh

# Make executable if needed
chmod +x scripts/verify-deployer.sh
```

**Expected Output**:
```
[INFO] Starting enhanced deployer verification
[PASS] Conan is available (version: 2.21.0)
[PASS] Enhanced deployer found at /home/user/.conan2/extensions/deployers/full_deploy_enhanced.py
...
[PASS] All tests passed!
```

## Running All Verification Scripts

### Individual Scripts

```bash
# Test bootstrap script
./scripts/verify-bootstrap.sh

# Test custom commands
python3 scripts/verify-commands.py

# Test enhanced deployer
./scripts/verify-deployer.sh
```

### Combined Verification

```bash
# Run all verification scripts
cd /path/to/openssl-devenv

echo "=== Bootstrap Verification ==="
./scripts/verify-bootstrap.sh

echo "=== Commands Verification ==="
python3 scripts/verify-commands.py

echo "=== Deployer Verification ==="
./scripts/verify-deployer.sh
```

## Success Criteria

### Bootstrap Verification
- ✅ All 12 tests pass
- ✅ Bootstrap script is syntactically correct
- ✅ All modes (minimal, full, dev) work in dry-run
- ✅ Fresh installation succeeds
- ✅ Idempotency works (can run twice)

### Commands Verification
- ✅ All 6 tests pass
- ✅ Custom commands are visible in `conan --help`
- ✅ `conan openssl:build --help` works
- ✅ `conan openssl:graph --help` works
- ✅ Graph analyzer produces valid JSON

### Deployer Verification
- ✅ All 11 tests pass
- ✅ Enhanced deployer is available
- ✅ Deploy folder structure is correct
- ✅ SBOM generation works (CycloneDX format)
- ✅ Metadata generation works
- ✅ Performance is acceptable (<5 minutes)

## CI Integration

### GitHub Actions

```yaml
name: Verification Tests

on: [push, pull_request]

jobs:
  verify-bootstrap:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run bootstrap verification
        run: ./scripts/verify-bootstrap.sh

  verify-commands:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install Conan
        run: pip install conan==2.21.0
      - name: Run commands verification
        run: python3 scripts/verify-commands.py

  verify-deployer:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install Conan
        run: pip install conan==2.21.0
      - name: Install extensions
        run: |
          mkdir -p ~/.conan2/extensions
          cp -r openssl-tools/extensions/* ~/.conan2/extensions/
      - name: Run deployer verification
        run: ./scripts/verify-deployer.sh
```

### Local Development

```bash
# Quick verification during development
./scripts/verify-bootstrap.sh && echo "Bootstrap OK" || echo "Bootstrap FAILED"

# Full verification
./scripts/verify-bootstrap.sh && \
python3 scripts/verify-commands.py && \
./scripts/verify-deployer.sh && \
echo "All verifications passed!" || echo "Some verifications failed"
```

## Troubleshooting

### Common Issues

**Q: "Bootstrap script not found"**
```bash
# Check if script exists and is executable
ls -la bootstrap/openssl-conan-init.py
chmod +x bootstrap/openssl-conan-init.py
```

**Q: "Conan command not found"**
```bash
# Install Conan first
pip install conan==2.21.0

# Or use full path
python3 scripts/verify-commands.py --conan-path /usr/local/bin/conan
```

**Q: "Enhanced deployer not found"**
```bash
# Check if extensions are installed
ls -la ~/.conan2/extensions/deployers/

# Install extensions if missing
mkdir -p ~/.conan2/extensions
cp -r openssl-tools/extensions/* ~/.conan2/extensions/
```

**Q: "Tests fail in CI but pass locally"**
```bash
# Check environment differences
echo "Python: $(python3 --version)"
echo "Conan: $(conan --version)"
echo "OS: $(uname -a)"
echo "PATH: $PATH"
```

### Debug Mode

Add debug output to scripts:

```bash
# Enable bash debug mode
set -x
./scripts/verify-bootstrap.sh

# Enable Python debug mode
python3 -v scripts/verify-commands.py
```

## Expected Outputs

### Successful Run

```
=== Bootstrap Verification ===
[INFO] Starting bootstrap script verification
[PASS] Bootstrap script exists and is executable
[PASS] Bootstrap script syntax is valid
...
[PASS] All tests passed!

=== Commands Verification ===
🔧 Checking Conan installation
✅ Conan 2.21.0 is installed and accessible
...
✅ All tests passed!

=== Deployer Verification ===
[INFO] Starting enhanced deployer verification
[PASS] Conan is available (version: 2.21.0)
...
[PASS] All tests passed!
```

### Failed Run

```
=== Bootstrap Verification ===
[FAIL] Bootstrap script not found: /path/to/bootstrap/openssl-conan-init.py
[INFO] Verification Summary:
[PASS] Tests passed: 0
[FAIL] Tests failed: 1
```

## Performance Expectations

- **Bootstrap verification**: <2 minutes
- **Commands verification**: <1 minute
- **Deployer verification**: <5 minutes
- **Total verification time**: <8 minutes

## Maintenance

### Adding New Tests

1. **Bootstrap tests**: Add to `verify-bootstrap.sh`
2. **Command tests**: Add to `verify-commands.py`
3. **Deployer tests**: Add to `verify-deployer.sh`

### Updating Success Criteria

Update this document when:
- New tests are added
- Success criteria change
- Performance expectations change
- New platforms are supported

## Related Documentation

- [Bootstrap Script README](../bootstrap/README.md)
- [Getting Started Guide](getting-started.md)
- [Architecture Overview](architecture.md)
- [Troubleshooting Guide](troubleshooting.md)




