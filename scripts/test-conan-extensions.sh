#!/bin/bash
set -e

echo "Testing Conan extensions integration..."

# 1. Install openssl-tools
cd openssl-tools
conan export . openssl-tools/1.2.0@
conan config install . -sf extensions -tf extensions

# 2. Build OpenSSL with deployer
cd ../openssl
conan openssl:build --fips --deployer-folder=./test-deploy

# 3. Verify artifacts
test -f test-deploy/sbom.json || { echo "SBOM missing"; exit 1; }
test -d test-deploy/full_deploy || { echo "Deploy folder missing"; exit 1; }
test -d test-deploy/fips || { echo "FIPS folder missing"; exit 1; }

# 4. Graph analysis
conan openssl:graph --json > graph.json
test -s graph.json || { echo "Graph analysis failed"; exit 1; }

echo "✅ All tests passed"
