# OpenSSL CI/CD Modernization - Architecture Diagram

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

```


## 🏗️ Corrected Architecture

```mermaid
graph TD
    %% Foundation Layer
    subgraph "🔐 Foundation Layer"
        BASE["openssl-conan-base<br>1.0.0<br>(Foundation Utils)"]
        FIPS["openssl-fips-policy<br>140-3.1<br>(FIPS Data + Certs)"]
    end

    %% Tooling Layer
    subgraph "🛠️ Tooling Layer"
        TOOLS["openssl-tools<br>1.0.0<br>(Build Orchestration)"]
    end

    %% Domain Layer
    subgraph "🌐 Domain Layer"
        OPENSSL["sparesparrow/openssl<br>3.4.1<br>(Forked Lib)"]
    end

    %% Distribution (Artifacts)
    subgraph "📦 Distribution"
        CLOUDSMITH["Cloudsmith<br>sparesparrow-conan/openssl-conan"]
    end

    %% Build Profiles
    subgraph "🎯 Build Profiles"
        P1["linux-gcc-release"]
        P2["linux-clang-release"]
        P3["windows-msvc2022"]
        P4["macos-arm64"]
        P5["macos-x86_64"]
        P6["fips-linux-gcc-release"]
    end

    %% CI Pipeline
    subgraph "🔄 CI/CD Pipeline"
        GHA["GitHub Actions"]
        BUILD["Build Matrix"]
        TEST["Testing Suite"]
        PUBLISH["Publish to Cloudsmith"]
    end

    %% Relations
    BASE --> CLOUDSMITH
    FIPS --> CLOUDSMITH
    TOOLS -.-> BASE
    TOOLS -.-> FIPS
    TOOLS --> CLOUDSMITH
    OPENSSL -.-> TOOLS
    OPENSSL -.-> FIPS
    OPENSSL --> CLOUDSMITH

    P1 --> BASE
    P1 --> FIPS
    P1 --> TOOLS
    P1 --> OPENSSL

    GHA --> BUILD
    BUILD --> TEST
    TEST --> PUBLISH
    PUBLISH --> CLOUDSMITH
```

## Key Components

### Foundation Layer
- **openssl-conan-base**: Core utilities, profiles, and Python environment
- **openssl-fips-policy**: FIPS 140-3 certificates and compliance data

### Tooling Layer
- **openssl-tools**: Build orchestration, automation scripts, and infrastructure

### Domain Layer
- **sparesparrow/openssl**: Forked OpenSSL library with Conan integration

### Distribution
- **Cloudsmith**: Package repository for all OpenSSL components

### Build Profiles
- **6 Standard Profiles**: Cross-platform support for Linux, Windows, macOS
- **FIPS Compliance**: Specialized profile for FIPS 140-3 requirements

### CI/CD Pipeline
- **GitHub Actions**: Automated build, test, and publish workflows
- **Build Matrix**: Multi-platform testing and validation
- **Security**: SBOM generation and compliance checking

