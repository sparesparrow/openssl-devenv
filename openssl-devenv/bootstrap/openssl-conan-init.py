#!/usr/bin/env python3
"""
OpenSSL Conan Bootstrap Script
Standalone installer - no pip dependencies required

Usage:
    python openssl-conan-init.py [--minimal|--full|--dev]
"""

import subprocess
import sys
import os
import platform
import urllib.request
import json
from pathlib import Path

__version__ = "1.0.0"

class Colors:
    """ANSI color codes"""
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_step(msg):
    print(f"{Colors.BLUE}{Colors.BOLD}➜{Colors.RESET} {msg}")

def print_success(msg):
    print(f"{Colors.GREEN}✓{Colors.RESET} {msg}")

def print_warning(msg):
    print(f"{Colors.YELLOW}⚠{Colors.RESET} {msg}")

def print_error(msg):
    print(f"{Colors.RED}✗{Colors.RESET} {msg}")

def check_python_version():
    """Ensure Python 3.8+"""
    if sys.version_info < (3, 8):
        print_error(f"Python 3.8+ required, found {sys.version}")
        sys.exit(1)
    print_success(f"Python {sys.version_info.major}.{sys.version_info.minor}")

def install_conan():
    """Install Conan 2.21.0 if not present (pin for reproducibility)"""
    print_step("Checking Conan installation...")

    try:
        result = subprocess.run(
            ["conan", "--version"],
            capture_output=True,
            text=True,
            check=True
        )
        version = result.stdout.strip()
        print_success(f"Conan already installed: {version}")

        # Enforce Conan 2.21.x pin
        if not version.startswith("Conan version 2.21."):
            print_warning("Pinning Conan to 2.21.0 for consistency...")
            subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "conan==2.21.0"], check=True)

        return True

    except (subprocess.CalledProcessError, FileNotFoundError):
        print_warning("Conan not found, installing pinned version 2.21.0...")
        subprocess.run([sys.executable, "-m", "pip", "install", "conan==2.21.0"], check=True)
        print_success("Conan 2.21.0 installed")
        return True

def setup_conan_remotes():
    """Configure Conan remotes"""
    print_step("Configuring Conan remotes...")

    remotes = [
        ("sparesparrow-conan", "https://cloudsmith.io/~sparesparrow-conan/repos/openssl-conan/"),
        ("conancenter", "https://center.conan.io")
    ]

    for name, url in remotes:
        try:
            # Check if remote exists
            result = subprocess.run(
                ["conan", "remote", "list"],
                capture_output=True,
                text=True,
                check=True
            )

            if name in result.stdout:
                print_success(f"Remote '{name}' already configured")
            else:
                subprocess.run(
                    ["conan", "remote", "add", name, url],
                    check=True
                )
                print_success(f"Added remote '{name}'")

        except subprocess.CalledProcessError as e:
            print_error(f"Failed to add remote '{name}': {e}")

def clone_or_update_repo(repo_name, org="sparesparrow"):
    """Clone or update a repository"""
    repo_path = Path.home() / "sparesparrow" / repo_name
    repo_url = f"https://github.com/{org}/{repo_name}.git"

    if repo_path.exists():
        print_step(f"Updating {repo_name}...")
        subprocess.run(
            ["git", "-C", str(repo_path), "pull"],
            check=True,
            capture_output=True
        )
        print_success(f"{repo_name} updated")
    else:
        print_step(f"Cloning {repo_name}...")
        repo_path.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(
            ["git", "clone", repo_url, str(repo_path)],
            check=True,
            capture_output=True
        )
        print_success(f"{repo_name} cloned")

    return repo_path

def install_openssl_tools():
    """Install openssl-tools python_requires"""
    print_step("Installing openssl-tools python_requires...")

    # Use the local openssl-tools from the workspace
    workspace_root = Path(__file__).parent.parent.parent  # Go up to openssl-devenv
    tools_path = workspace_root / "openssl-tools"

    if not tools_path.exists():
        print_error(f"openssl-tools not found at {tools_path}")
        print_error("Please ensure openssl-tools is cloned in the workspace")
        sys.exit(1)

    # Export python_requires
    subprocess.run(
                ["conan", "export", str(tools_path), "--name=openssl-tools", "--version=1.2.0"],
        check=True,
        capture_output=True
    )

    # Install extensions
    subprocess.run(
        ["conan", "config", "install", str(tools_path),
         "-sf", "extensions", "-tf", "extensions"],
        check=True,
        capture_output=True
    )

    print_success("openssl-tools installed")

def install_profiles():
    """Install Conan profiles"""
    print_step("Installing Conan profiles...")

    base_path = clone_or_update_repo("openssl-conan-base")

    subprocess.run(
        ["conan", "config", "install", str(base_path),
         "-sf", "profiles", "-tf", "profiles"],
        check=True,
        capture_output=True
    )

    print_success("Profiles installed")

def setup_ide_integration():
    """Setup IDE integration helpers"""
    print_step("Setting up IDE integration...")

    vscode_settings = Path.cwd() / ".vscode" / "settings.json"
    vscode_settings.parent.mkdir(exist_ok=True)

    settings = {
        "cmake.configureArgs": [
            "-DCMAKE_MODULE_PATH=${workspaceFolder}/build",
            "-DCMAKE_EXPORT_COMPILE_COMMANDS=ON"
        ],
        "C_Cpp.default.compileCommands": "${workspaceFolder}/build/compile_commands.json",
        "conan.buildType": "Release",
        "files.associations": {
            "conanfile.py": "python",
            "conandata.yml": "yaml"
        }
    }

    if vscode_settings.exists():
        with open(vscode_settings, 'r') as f:
            existing = json.load(f)
        existing.update(settings)
        settings = existing

    with open(vscode_settings, 'w') as f:
        json.dump(settings, f, indent=2)

    print_success("VS Code settings configured")

def create_workspace_config():
    """Create workspace configuration"""
    print_step("Creating workspace configuration...")

    config = {
        "workspace": "sparesparrow-openssl",
        "repos": {
            "openssl-tools": str(Path.home() / "sparesparrow" / "openssl-tools"),
            "openssl-conan-base": str(Path.home() / "sparesparrow" / "openssl-conan-base"),
            "openssl": str(Path.home() / "sparesparrow" / "openssl"),
            "openssl-fips-policy": str(Path.home() / "sparesparrow" / "openssl-fips-policy")
        },
        "conan_version": "2.21.0",
        "cloudsmith_url": "https://cloudsmith.io/~sparesparrow-conan/"
    }

    config_path = Path.home() / ".sparesparrow-openssl-config.json"
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)

    print_success(f"Workspace config saved to {config_path}")

def print_next_steps():
    """Print helpful next steps"""
    print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 Setup Complete!{Colors.RESET}\n")
    print("Next steps:")
    print(f"  1. Build OpenSSL with FIPS: {Colors.BLUE}conan openssl:build --fips{Colors.RESET}")
    print(f"  2. Analyze dependencies: {Colors.BLUE}conan openssl:graph --json{Colors.RESET}")
    print(f"  3. Open VS Code in project directory")
    print(f"\nDocumentation: {Colors.BLUE}https://github.com/sparesparrow/openssl-tools/README.md{Colors.RESET}")

def main():
    """Main bootstrap flow"""
    print(f"{Colors.BOLD}OpenSSL Conan Bootstrap v{__version__}{Colors.RESET}\n")

    check_python_version()
    install_conan()
    setup_conan_remotes()

    mode = sys.argv[1] if len(sys.argv) > 1 else "--full"

    if mode in ["--full", "--dev"]:
        clone_or_update_repo("openssl-tools")
        clone_or_update_repo("openssl-conan-base")
        clone_or_update_repo("openssl")
        clone_or_update_repo("openssl-fips-policy")

    install_openssl_tools()
    install_profiles()

    if mode == "--dev":
        setup_ide_integration()
        create_workspace_config()

    print_next_steps()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_error("\nAborted by user")
        sys.exit(1)
    except Exception as e:
        print_error(f"Setup failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
