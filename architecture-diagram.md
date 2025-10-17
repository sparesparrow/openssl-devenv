# OpenSSL CI/CD Modernization - Architecture Diagram

## 🏗️ Corrected Architecture

```mermaid
graph TD
    subgraph Foundation["🔐 Foundation Layer" style fill:#e1f5fe]
        BASE[openssl-conan-base<br/>1.0.0<br/>(Foundation Utils)]
        FIPS[openssl-fips-policy<br/>140-3.1<br/>(FIPS Data + Certs)]
    end
    
    subgraph Tooling["🛠️ Tooling Layer" style fill:#fff3e0]
        TOOLS[openssl-tools<br/>1.0.0<br/>(Build Orchestration)]
    end
    
    subgraph Domain["🌐 Domain Layer" style fill:#f3e5f5]
        OPENSSL[sparesparrow/openssl<br/>3.4.1<br/>(Forked Lib)]
    end
    
    subgraph Artifacts["📦 Distribution" style fill:#e8f5e9]
        CLOUDSMITH[(Cloudsmith<br/>sparesparrow-conan/openssl-conan)]
    end
    
    subgraph Profiles["🎯 Build Profiles" style fill:#fce4ec]
        P1[linux-gcc-release]
        P2[linux-clang-release]
        P3[windows-msvc2022]
        P4[macos-arm64]
        P5[macos-x86_64]
        P6[fips-linux-gcc-release]
    end
    
    subgraph CI["🔄 CI/CD Pipeline" style fill:#f1f8e9]
        GHA[GitHub Actions]
        BUILD[Build Matrix]
        TEST[Testing Suite]
        PUBLISH[Publish to Cloudsmith]
    end
    
    BASE --> CLOUDSMITH
    FIPS --> CLOUDSMITH
    TOOLS -.requires.-> BASE
    TOOLS -.requires.-> FIPS
    TOOLS --> CLOUDSMITH
    OPENSSL -.tool_requires.-> TOOLS
    OPENSSL -.requires.-> FIPS
    OPENSSL --> CLOUDSMITH
    
    P1 --> BASE
    P1 --> FIPS
    P1 --> TOOLS
    P1 --> OPENSSL
    
    P2 --> BASE
    P2 --> FIPS
    P2 --> TOOLS
    P2 --> OPENSSL
    
    P3 --> BASE
    P3 --> FIPS
    P3 --> TOOLS
    P3 --> OPENSSL
    
    P4 --> BASE
    P4 --> FIPS
    P4 --> TOOLS
    P4 --> OPENSSL
    
    P5 --> BASE
    P5 --> FIPS
    P5 --> TOOLS
    P5 --> OPENSSL
    
    P6 --> BASE
    P6 --> FIPS
    P6 --> TOOLS
    P6 --> OPENSSL
    
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

