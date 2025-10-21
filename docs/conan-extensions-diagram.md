# Conan 2.x Extensions Architecture & Workflow Diagram

## File Explanations

### Core Package Files

**`🛠️ Tooling: OpenSSL Tools/conanfile.py`** - Main Python_requires Package
- **Purpose**: Defines `openssl-tools/1.2.0` as a python_requires package
- **Exports**: Extensions directory containing all Conan extensions
- **Provides**: `build_openssl()` method for OpenSSL build orchestration
- **Usage**: Other recipes use `python_requires = "openssl-tools/1.2.0"`

**`🛠️ Tooling: OpenSSL Tools/test_package/conanfile.py`** - Package Validation
- **Purpose**: Tests that python_requires functionality works correctly
- **Validates**: Extensions are properly accessible after installation
- **Usage**: `conan create test_package` validates the package

### Extension Files

**`🛠️ Tooling: OpenSSL Tools/extensions/deployers/full_deploy_enhanced.py`** - Enhanced Deployer
- **Purpose**: Custom Conan deployer with SBOM generation and FIPS support
- **Features**:
  - Generates CycloneDX format SBOMs
  - Deploys FIPS artifacts (fipsmodule.cnf)
  - Creates complete deployment bundles in `full_deploy/` structure
- **Usage**: `--deployer=full_deploy_enhanced`

**`🛠️ Tooling: OpenSSL Tools/extensions/graph/analyzer.py`** - Dependency Analyzer
- **Purpose**: Analyzes Conan dependency graphs for conflicts and FIPS status
- **Features**:
  - Detects FIPS-enabled packages
  - Identifies dependency conflicts
  - Provides structured analysis results
- **Usage**: Integrated into `conan openssl:graph` command

### Command Extensions

**`🛠️ Tooling: OpenSSL Tools/extensions/commands/openssl/cmd_build.py`** - Build Command
- **Purpose**: `conan openssl:build` - simplified OpenSSL build orchestration
- **Features**:
  - Handles FIPS mode configuration
  - Uses enhanced deployer automatically
  - Supports custom profiles and deployment folders
- **Usage**: `conan openssl:build --fips --profile=linux-gcc11-fips`

**`🛠️ Tooling: OpenSSL Tools/extensions/commands/openssl/cmd_graph.py`** - Graph Command
- **Purpose**: `conan openssl:graph` - dependency analysis and visualization
- **Features**:
  - Human-readable output format
  - JSON output for automation
  - FIPS package detection
- **Usage**: `conan openssl:graph --json > dependencies.json`

### CI/CD Integration

**`🛠️ Tooling: OpenSSL Tools/.github/workflows/openssl-ci-reusable.yml`** - Reusable CI Workflow
- **Purpose**: Reusable GitHub Actions workflow for OpenSSL builds
- **Features**:
  - Multi-platform support (Linux/Windows/macOS)
  - Configurable build options (shared, FIPS)
  - Artifact upload and management
- **Usage**: Called by other repositories via `workflow_call`

**`🛠️ Tooling: OpenSSL Tools/.github/workflows/trigger-openssl.yml`** - Integration Trigger
- **Purpose**: Triggers OpenSSL repository workflows when tools are updated
- **Features**:
  - Automatic triggering on main branch pushes
  - Manual trigger support for testing
  - Cross-repository workflow dispatch
- **Usage**: Automatically runs when openssl-tools changes

### Platform Configuration

**`🛠️ Tooling: OpenSSL Tools/conan-dev/platform-config.yml`** - Development Environment Config
- **Purpose**: Configuration for local Conan development environment
- **Features**:
  - Platform-specific settings
  - Profile management
  - Script and launcher configuration
- **Usage**: Used by development tools and scripts

### Upload & Distribution

**`🛠️ Tooling: OpenSSL Tools/scripts/upload-conan-package.py`** - Package Upload Script
- **Purpose**: Uploads Conan packages to GitHub releases as assets
- **Features**:
  - Creates ZIP archives of packages
  - Generates GitHub releases with package metadata
  - Supports user/channel references
- **Usage**: `./scripts/upload-conan-package.py --github-owner sparesparrow --github-repo openssl-tools`

### Runtime Environment

**`🛠️ Tooling: OpenSSL Tools/build-release/conan/conanrunenv-release-x86_64.sh`** - Runtime Environment
- **Purpose**: Sets up runtime environment variables for Conan packages
- **Features**:
  - Configures OPENSSL_PROFILES_PATH
  - Sets up FIPS_DATA_ROOT for FIPS builds
  - Provides environment cleanup script

## Architecture Flow Diagram

```mermaid
graph TB
    subgraph "🔧 Core Package"
        A[🛠️ conanfile.py<br/>Python_requires Package]
        B[🛠️ test_package/conanfile.py<br/>Package Validation]
    end

    subgraph "📦 Extensions"
        C[🛠️ full_deploy_enhanced.py<br/>Enhanced Deployer<br/>SBOM + FIPS]
        D[🛠️ analyzer.py<br/>Graph Analyzer<br/>Conflict Detection]
    end

    subgraph "🎮 Commands"
        E[🛠️ cmd_build.py<br/>openssl:build<br/>Simplified Builds]
        F[🛠️ cmd_graph.py<br/>openssl:graph<br/>Dependency Analysis]
    end

    subgraph "🔄 CI/CD Integration"
        G[🛠️ openssl-ci-reusable.yml<br/>Reusable Workflow<br/>Multi-Platform]
        H[🛠️ trigger-openssl.yml<br/>Cross-Repo Trigger<br/>Integration Tests]
    end

    subgraph "⚙️ Configuration"
        I[🛠️ platform-config.yml<br/>Dev Environment<br/>Profile Management]
    end

    subgraph "📤 Distribution"
        J[🛠️ upload-conan-package.py<br/>GitHub Release<br/>Package Distribution]
    end

    subgraph "🔧 Runtime"
        K[🛠️ conanrunenv-release-x86_64.sh<br/>Runtime Environment<br/>Variable Setup]
    end

    %% Core Package Relations
    A --> B
    A --> C
    A --> D
    A --> E
    A --> F

    %% Extension Relations
    C --> J
    D --> F

    %% Command Relations
    E --> C
    F --> D

    %% CI/CD Relations
    G --> E
    H --> G

    %% Configuration Relations
    I --> G

    %% Runtime Relations
    K --> C

    %% Workflow Descriptions
    subgraph "🔄 Build Workflow"
        direction TB
        A1[1. Load python_requires<br/>openssl-tools/1.2.0]
        A2[2. Configure with options<br/>--fips --profile]
        A3[3. Build with orchestration<br/>build_openssl()]
        A4[4. Deploy with enhanced deployer<br/>SBOM + artifacts]
        A5[5. Package for distribution<br/>GitHub releases]

        A1 --> A2 --> A3 --> A4 --> A5
    end

    subgraph "📊 Analysis Workflow"
        direction TB
        B1[1. Load dependency graph<br/>conanfile.txt/conanfile.py]
        B2[2. Analyze with analyzer.py<br/>Conflicts & FIPS status]
        B3[3. Generate report<br/>JSON/Human readable]
        B4[4. Export results<br/>CI integration]

        B1 --> B2 --> B3 --> B4
    end

    subgraph "🚀 CI/CD Workflow"
        direction TB
        C1[1. Trigger on changes<br/>conanfile.py updates]
        C2[2. Multi-platform build<br/>Linux/Windows/macOS]
        C3[3. Enhanced deployment<br/>SBOM + security scan]
        C4[4. Artifact management<br/>Cloudsmith + GitHub]

        C1 --> C2 --> C3 --> C4
    end

    %% Styling
    classDef primary fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    classDef secondary fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    classDef tertiary fill:#e8f5e8,stroke:#1b5e20,stroke-width:2px

    class A,B primary
    class C,D,E,F secondary
    class G,H,I,J,K tertiary
```

## Workflow Integration Points

### 🔄 **Build Workflow**
1. **Entry Point**: `conan openssl:build --fips`
2. **Python Requires**: Loads `openssl-tools/1.2.0`
3. **Build Orchestration**: Uses `build_openssl()` method
4. **Enhanced Deployment**: `full_deploy_enhanced` creates bundles
5. **Artifact Management**: Upload script creates GitHub releases

### 📊 **Analysis Workflow**
1. **Entry Point**: `conan openssl:graph --json`
2. **Graph Loading**: Parses conanfile.txt/conanfile.py
3. **Analysis Engine**: `analyzer.py` detects conflicts and FIPS
4. **Output Generation**: Human-readable or JSON format
5. **CI Integration**: Results feed into security scanning

### 🚀 **CI/CD Workflow**
1. **Trigger**: Changes to conanfile.py files
2. **Reusable Workflows**: `openssl-ci-reusable.yml` handles builds
3. **Cross-Repo Sync**: `trigger-openssl.yml` notifies dependent repos
4. **Platform Matrix**: Linux/Windows/macOS builds
5. **Security Integration**: SBOM generation and vulnerability scanning

## File Relations Summary

| File | Purpose | Workflow Integration | Dependencies |
|------|---------|---------------------|-------------|
| **conanfile.py** | Python_requires hub | All workflows | Extensions |
| **full_deploy_enhanced.py** | Enhanced deployment | Build workflow | conanfile.py |
| **analyzer.py** | Graph analysis | Analysis workflow | conanfile.py |
| **cmd_build.py** | Build command | Build workflow | conanfile.py |
| **cmd_graph.py** | Graph command | Analysis workflow | analyzer.py |
| **openssl-ci-reusable.yml** | CI workflow | CI/CD workflow | cmd_build.py |
| **platform-config.yml** | Dev environment | Local development | All files |
| **upload-conan-package.py** | Package distribution | CI/CD workflow | Built packages |
| **trigger-openssl.yml** | Integration trigger | CI/CD workflow | Repository changes |

This architecture provides a comprehensive, integrated Conan 2.x ecosystem for OpenSSL development with seamless CI/CD integration and enhanced security compliance.



