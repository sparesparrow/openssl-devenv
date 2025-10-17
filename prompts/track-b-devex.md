# Track B: Developer Experience & Onboarding Implementation

## Goal
Create zero-friction onboarding for sparesparrow OpenSSL developers.

## Context
- Current state: Conan extensions working (openssl:build, openssl:graph)
- Target: < 15 minute onboarding for new developers
- Platform support: Linux, macOS, Windows WSL

## Deliverables

### 1. Bootstrap Script (openssl-devenv/bootstrap/openssl-conan-init.py)
Standalone Python 3.8+ script with:
- Auto-detect and install Conan 2.x if missing
- Configure remotes (sparesparrow-conan, conancenter)
- Clone/update all repos (use ~/sparesparrow/ directory)
- Install openssl-tools extensions via install-extensions.sh
- Modes: --minimal (Conan only), --full (repos), --dev (IDE)
- Colored progress indicators (use ANSI codes)
- Error handling with actionable fixes

### 2. VS Code Integration (openssl-devenv/.vscode/)
- extensions.json: Recommended extensions (C/C++, CMake, Python, Conan)
- settings.json: Workspace settings (paths, IntelliSense)
- launch.json: Debug configs (OpenSSL CLI, FIPS self-test, Python recipes)
- tasks.json: Build/test/clean tasks

### 3. IntelliSense Helper (openssl-devenv/scripts/update-intellisense.py)
- Extract include paths from Conan dependencies
- Update c_cpp_properties.json automatically
- Support for cross-compilation toolchains

### 4. Documentation (openssl-devenv/docs/)
- getting-started.md: Quick start, common tasks, troubleshooting
- architecture.md: Repo relationships, diagrams

## Implementation Constraints
- Bootstrap MUST be standalone (no pip install until Conan is ready)
- Use pathlib not os.path
- Cross-platform (Linux/macOS/Windows WSL)
- Idempotent (safe to run multiple times)

## Testing Requirements
- Test on fresh Ubuntu 22.04 VM
- Verify < 15 minute onboarding time
- VS Code IntelliSense works immediately after bootstrap
- Debugging with breakpoints functional

## Success Criteria
- [ ] Bootstrap script completes in < 15 minutes on fresh system
- [ ] VS Code opens project with working IntelliSense
- [ ] Debugging OpenSSL CLI works with breakpoints
- [ ] Documentation covers 90% of common questions
