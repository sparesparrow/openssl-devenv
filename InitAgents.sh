#!/bin/bash




for dir in openssl-tools openssl-conan-base openssl-fips-policy openssl openssl-conan openssl-ci openssl-docker; do
  if [ -d "$dir" ]; then
    echo "Processing $dir..."
    cd "$dir"
    
    case "$dir" in
      openssl-tools)
        cursor-agent -p "Validate python_requires package structure: verify conanfile.py exports shared utilities per Conan 2.0 docs, test bootstrap openssl-conan-init.py with zero pip dependencies, run conan create . --version=0.1.0 --user=_ --channel=_, execute pytest tests/integration/test_python_requires_consumer.py with >95% coverage on src/openssl_tools/, generate SBOM via syft packages dir:. -o spdx-json > sbom-tools.json, security scan trivy fs --severity HIGH,CRITICAL --exit-code 1 ., create temp consumer conanfile importing openssl-tools/0.1.0 base classes, test custom command conan openssl-profile-generate linux-gcc11 verifying ~/.conan2/profiles/linux-gcc11 creation, validate Cloudsmith publish workflow mock CLOUDSMITH_API_KEY and conan upload openssl-tools/0.1.0 -r=sparesparrow-conan, verify cache symlink ~/.conan2/p/ to /OSSL/ persistence, simulate GitHub Actions via act -j python-requires-publish --secret CLOUDSMITH_API_KEY=dummy, assert zero HIGH/CRITICAL vulnerabilities CI runtime <3 minutes" --output-format json > "../${dir}-agent.json" &
        ;;
      
      openssl-conan-base)
        cursor-agent -p "Validate cross-platform profiles and base recipe consuming openssl-tools python_requires: install profiles via conan config install profiles/ -tf profiles then conan profile show linux-gcc11, verify platform matrix linux-gcc11 Ubuntu 22.04 GCC 11.4, windows-msvc193 VS 2022 MSVC 19.3, macos-arm64 macOS 14 Apple Clang 15, run dependency resolution conan install . --profile=linux-gcc11 --build=missing --format=json > install.json, validate python_requires via jq '.graph.nodes[] | select(.ref | contains("openssl-tools"))' install.json, generate dependency graph conan graph info . --profile=linux-gcc11 --format=json checking no circular dependencies, test /OSSL/ symlink strategy sudo mkdir -p /OSSL && sudo chown $(whoami) /OSSL then ln -sf ~/.conan2/p /OSSL/cache/packages, verify ls -la /OSSL/cache/packages/openssl*/p/, execute cross-platform matrix act -j test-matrix --matrix os:ubuntu-22.04,windows-2022,macos-14 --matrix profile:linux-gcc11,windows-msvc193,macos-arm64, generate SBOM syft packages . -o cyclonedx-json > sbom-base.json verifying python_requires inheritance jq '.packages[] | select(.name=="openssl-tools")', security scan trivy config . --severity HIGH,CRITICAL, test symlink persistence after conan cache clean "*" --source --build, assert all 3 platforms succeed python_requires resolved from https://cloudsmith.io/~sparesparrow-conan/repos/openssl-conan/packages/ runtime <5min per platform" --output-format json > "../${dir}-agent.json" &
        ;;
      
      openssl-fips-policy)
        cursor-agent -p "Automate FIPS 140-3 module validation and compliance: build FIPS-enabled OpenSSL conan create . --name=openssl-fips --version=3.0.8 --profile=linux-gcc11 -o fips=True, locate FIPS module export OPENSSL_MODULES=$(find ~/.conan2/p/openssl* -name '*.so' -path '*/ossl-modules/*'), verify self-tests openssl fipsinstall -verify -module $OPENSSL_MODULES/fips.so, generate per-platform fipsmodule.cnf via openssl fipsinstall -out fipsmodule.cnf -module $OPENSSL_MODULES/fips.so parsing install-status = INSTALL_SELF_TEST_KATS_RUN with HMAC-SHA256 checksum validation, test cross-machine enforcement on ubuntu-22.04 ubuntu-24.04 windows-2022 macos-14 via docker/act matrix ensuring no fipsmodule.cnf file reuse between runners, activate FIPS mode export OPENSSL_CONF=$(find ~/.conan2/p/openssl* -name openssl.cnf) then test algorithm restrictions openssl sha256 -provider fips -in testfile.txt must succeed, openssl md5 -in testfile.txt must fail with FIPS error, validate approved algorithms AES-256-GCM SHA-256 SHA-384 RSA-2048 ECDSA-P256 available, verify deprecated APIs rejected compile gcc test_deprecated.c -lcrypto -Werror=deprecated-declarations for EVP_MD_CTX_new RSA_sign ENGINE_* expecting compilation failures, run CodeQL scan with .github/codeql/fips-deprecation-check.ql detecting zero deprecated usages, generate SBOM syft packages . -o spdx-json extracting CMVP certificate number jq '.packages[] | select(.name | contains("openssl")) | .version', security scan trivy config . --policy .trivyignore --severity CRITICAL, assert self-tests pass all platforms no config reuse MD5/RC4/DES unavailable in FIPS mode runtime <8min including self-test execution" --output-format json > "../${dir}-agent.json" &
        ;;
      
      openssl)
        cursor-agent -p "Validate OpenSSL fork or custom build: verify upstream sync with official openssl/openssl repository git remote -v checking origin and upstream, run comprehensive test suite make test ensuring all crypto algorithms functional, validate FIPS module availability if enabled ./config enable-fips && make && make test, generate build artifacts for Conan packaging, test cross-platform compilation ubuntu-22.04 windows-2022 macos-14 with different compilers gcc clang msvc, run security scan trivy fs . --severity HIGH,CRITICAL, generate SBOM syft packages dir:. -o spdx-json > sbom-openssl.json, verify CVE patches applied checking CHANGES.md and security advisories https://www.openssl.org/news/secadv.html, test integration with openssl-conan-base package consumption, assert zero HIGH/CRITICAL vulnerabilities all tests pass on 3 platforms" --output-format json > "../${dir}-agent.json" &
        ;;
      
      openssl-conan)
        cursor-agent -p "Validate Conan package recipe for OpenSSL: verify conanfile.py follows Conan 2.0 best practices, test package creation conan create . --version=3.0.8 --build=missing, validate options fips shared no_deprecated enable_quic enable_tls13, test profile application linux-gcc11 windows-msvc193 macos-arm64, verify library artifacts libssl libcrypto headers in package, run consumer test creating minimal app linking against OpenSSL via Conan, validate Cloudsmith upload conan upload openssl/3.0.8 -r=sparesparrow-conan, generate dependency graph conan graph info . ensuring no conflicts, test cross-compilation for ARM64 x86_64 architectures, run security scan trivy fs . --severity HIGH,CRITICAL, generate SBOM syft packages . -o cyclonedx-json, verify compatibility with openssl-tools python_requires consumption, assert package installable on all platforms zero HIGH/CRITICAL vulnerabilities runtime <10min" --output-format json > "../${dir}-agent.json" &
        ;;
      
      openssl-ci)
        cursor-agent -p "Validate CI/CD pipeline infrastructure: verify GitHub Actions workflows syntax .github/workflows/*.yml, test reusable workflows cross-repository consumption from openssl-tools openssl-conan-base openssl-fips-policy, validate matrix strategies platforms ubuntu-22.04 ubuntu-24.04 windows-2022 macos-14, test caching strategy Conan cache ~/.conan2/p/ symlink to /OSSL/, verify Cloudsmith publish workflow authentication CLOUDSMITH_API_KEY secret, test security scanning integration Trivy Syft CodeQL, validate artifact uploads release packages SBOMs, test failure notifications Slack email GitHub issues, run pipeline simulation locally act -j ci-matrix --matrix os:ubuntu-22.04,windows-2022, verify secrets management no leaked credentials in logs, test branch protection rules main develop branches, assert all workflows valid no syntax errors runtime <15min for full matrix" --output-format json > "../${dir}-agent.json" &
        ;;
      
      openssl-docker)
        cursor-agent -p "Validate Docker containerization for OpenSSL builds: verify Dockerfile multi-stage build efficiency, test base images ubuntu:22.04 alpine:3.18 debian:bookworm, validate OpenSSL compilation inside container ./config && make && make install, verify FIPS module availability in containerized builds, test dev container devcontainer.json for VS Code/Cursor integration, validate volume mounts ~/.conan2:/root/.conan2 for cache persistence, test cross-platform images linux/amd64 linux/arm64, run security scan trivy image --severity HIGH,CRITICAL, generate SBOM syft packages docker:openssl-build -o spdx-json, verify image size optimization < 500MB for production < 2GB for dev, test integration with openssl-ci GitHub Actions workflow docker build and push, validate registry publish ghcr.io/sparesparrow/openssl, test runtime environment variables OPENSSL_CONF OPENSSL_MODULES, assert images functional on Docker Kubernetes Podman zero HIGH/CRITICAL vulnerabilities" --output-format json > "../${dir}-agent.json" &
        ;;
      
      *)
        cursor-agent -p "Perform comprehensive repository analysis: identify primary language and tech stack, analyze directory structure and organization, review README.md documentation completeness, test build system make CMake Conan poetry npm, validate CI/CD configuration GitHub Actions GitLab CI, run security scan trivy fs . --severity HIGH,CRITICAL, generate SBOM syft packages . -o spdx-json, check licensing compliance SPDX identifiers, review code quality linting formatting, test integration with other sparesparrow openssl repositories, verify git history no sensitive data leaks, assert documentation exists build successful zero HIGH/CRITICAL vulnerabilities" --output-format json > "../${dir}-agent.json" &
        ;;
    esac
    
    cd ..
  fi
done

wait


cat  *-agent.json 
