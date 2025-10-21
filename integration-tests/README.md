# OpenSSL Integration Test Suite

This directory contains comprehensive integration tests that validate the OpenSSL Conan package ecosystem across multiple platforms and deployment targets.

## Test Categories

### 1. Consumer Project Tests
- **Basic Consumer**: Simple CMake project using OpenSSL
- **FIPS Consumer**: Project with FIPS mode enabled
- **Static Consumer**: Project using static OpenSSL libraries
- **Shared Consumer**: Project using shared OpenSSL libraries

### 2. Multi-Platform Tests
- **Linux GCC**: Ubuntu 22.04 with GCC 11
- **Linux Clang**: Ubuntu 22.04 with Clang 15
- **Windows MSVC**: Windows 2022 with MSVC 2022
- **macOS ARM64**: macOS 13 with Apple Clang
- **macOS x86_64**: macOS 13 with Apple Clang

### 3. Deployment Target Tests
- **General**: Standard OpenSSL build
- **FIPS Government**: FIPS 140-3 validated build
- **Embedded**: Optimized for embedded systems

### 4. Performance Benchmarks
- **Build Time**: Measure packaging overhead
- **Runtime Performance**: Cryptographic operation benchmarks
- **Memory Usage**: Memory footprint analysis

## Running Tests

### Local Testing
```bash
# Run all integration tests
./run-integration-tests.sh

# Run specific test category
./run-integration-tests.sh --category consumer
./run-integration-tests.sh --category platform
./run-integration-tests.sh --category deployment
./run-integration-tests.sh --category performance
```

### CI/CD Testing
Tests are automatically run in GitHub Actions workflows:
- **Consumer Tests**: On every PR
- **Platform Tests**: On main branch pushes
- **Deployment Tests**: On release tags
- **Performance Tests**: Weekly scheduled runs

## Test Results

Test results are published as:
- **GitHub Actions Artifacts**: Detailed logs and reports
- **GitHub Pages**: Performance trend charts
- **SARIF Reports**: Security and quality findings

## Adding New Tests

1. Create test directory: `integration-tests/test-<name>/`
2. Add `conanfile.py` and `CMakeLists.txt`
3. Update `run-integration-tests.sh` to include new test
4. Add test to appropriate CI workflow

## Troubleshooting

### Common Issues
- **Missing Dependencies**: Ensure all foundation packages are built
- **Version Conflicts**: Check version compatibility matrix
- **Platform Issues**: Verify platform-specific requirements

### Debug Mode
```bash
# Enable verbose output
./run-integration-tests.sh --verbose

# Run single test with debug
./run-integration-tests.sh --test basic-consumer --debug
```
