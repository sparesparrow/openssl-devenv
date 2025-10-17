FROM mcr.microsoft.com/devcontainers/base:ubuntu

# Install system dependencies for OpenSSL development
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends \
    build-essential \
    cmake \
    ninja-build \
    python3-dev \
    python3-pip \
    python3-venv \
    git \
    curl \
    wget \
    ca-certificates \
    libssl-dev \
    pkg-config \
    perl \
    zlib1g-dev \
    libzstd-dev \
    valgrind \
    gdb \
    lcov \
    clang-format \
    clang-tidy \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Conan
RUN pip3 install --upgrade pip \
    && pip3 install conan>=2.0.17

# Install development tools
RUN pip3 install \
    pytest \
    pytest-cov \
    pytest-asyncio \
    black \
    isort \
    flake8 \
    mypy \
    ruff \
    pre-commit

# Set up Python virtual environment structure
RUN mkdir -p /opt/venvs && python3 -m venv /opt/venvs/openssl-dev

# Create workspace directory
RUN mkdir -p /workspaces

# Set environment variables
ENV CONAN_USER_HOME=/home/vscode/.conan2
ENV PYTHONPATH=/workspaces
ENV PATH="/opt/venvs/openssl-dev/bin:$PATH"

# Create user and set permissions
RUN useradd -m -s /bin/bash vscode \
    && chown -R vscode:vscode /workspaces \
    && chown -R vscode:vscode /opt/venvs

USER vscode
WORKDIR /workspaces

# Initialize Conan
RUN conan profile detect

# Add Cloudsmith remote (will be configured with API key at runtime)
RUN conan remote add ${CONAN_REPOSITORY_NAME} \
    ${CONAN_REPOSITORY_URL} \
    --force || true
