#!/usr/bin/env python3
"""
OpenSSL Conan Development Environment Bootstrap Script

This script sets up a complete OpenSSL development environment with Conan 2.x,
custom extensions, and VS Code integration.

Usage:
    python3 openssl-conan-init.py [--minimal|--full|--dev] [--dry-run] [--test-mode]

Modes:
    --minimal: Install Conan 2.x and basic configuration (2-3 minutes)
    --full: Clone repositories and install extensions (8-12 minutes)  
    --dev: Full setup with VS Code integration (12-15 minutes)

Options:
    --dry-run: Show what would be done without making changes
    --test-mode: Run in test mode for CI validation
    --validate: Validate existing installation
"""

import argparse
import json
import os
import platform
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import urllib.request
import zipfile


class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'


class BootstrapError(Exception):
    """Custom exception for bootstrap errors"""
    pass


class OpenSSLConanBootstrap:
    """Main bootstrap class for OpenSSL Conan development environment"""
    
    def __init__(self, dry_run: bool = False, test_mode: bool = False):
        self.dry_run = dry_run
        self.test_mode = test_mode
        self.system = platform.system().lower()
        self.arch = platform.machine().lower()
        self.home_dir = Path.home()
        self.conan_dir = self.home_dir / '.conan2'
        self.extensions_dir = self.conan_dir / 'extensions'
        self.sparesparrow_dir = self.home_dir / 'sparesparrow'
        self.vscode_dir = Path('.vscode')
        
        # Repository URLs
        self.repos = {
            'openssl': 'https://github.com/sparesparrow/openssl.git',
            'openssl-tools': 'https://github.com/sparesparrow/openssl-tools.git',
            'openssl-conan-base': 'https://github.com/sparesparrow/openssl-conan-base.git',
            'openssl-fips-policy': 'https://github.com/sparesparrow/openssl-fips-policy.git',
            'openssl-devenv': 'https://github.com/sparesparrow/openssl-devenv.git'
        }
        
        # Conan configuration
        self.conan_version = '2.21.0'
        self.remotes = {
            'sparesparrow-conan': 'https://cloudsmith.io/~sparesparrow-conan/repos/openssl-conan/',
            'conancenter': 'https://center.conan.io'
        }
    
    def log(self, message: str, color: str = Colors.END) -> None:
        """Log a message with optional color"""
        if self.dry_run:
            print(f"{Colors.YELLOW}[DRY RUN]{Colors.END} {color}{message}{Colors.END}")
        else:
            print(f"{color}{message}{Colors.END}")
    
    def log_step(self, step: str) -> None:
        """Log a step with formatting"""
        self.log(f"\n{Colors.BOLD}🔧 {step}{Colors.END}")
    
    def log_success(self, message: str) -> None:
        """Log a success message"""
        self.log(f"✅ {message}", Colors.GREEN)
    
    def log_warning(self, message: str) -> None:
        """Log a warning message"""
        self.log(f"⚠️  {message}", Colors.YELLOW)
    
    def log_error(self, message: str) -> None:
        """Log an error message"""
        self.log(f"❌ {message}", Colors.RED)
    
    def run_command(self, cmd: List[str], cwd: Optional[Path] = None, 
                   capture_output: bool = False) -> Tuple[int, str, str]:
        """Run a command with optional dry-run mode"""
        if self.dry_run:
            self.log(f"Would run: {' '.join(cmd)}")
            return 0, "", ""
        
        try:
            result = subprocess.run(
                cmd, 
                cwd=cwd,
                capture_output=capture_output,
                text=True,
                check=False
            )
            return result.returncode, result.stdout, result.stderr
        except Exception as e:
            raise BootstrapError(f"Command failed: {' '.join(cmd)} - {e}")
    
    def check_python_version(self) -> None:
        """Check if Python version is compatible"""
        self.log_step("Checking Python version")
        
        if sys.version_info < (3, 8):
            raise BootstrapError("Python 3.8+ is required")
        
        self.log_success(f"Python {sys.version.split()[0]} is compatible")
    
    def check_conan_installation(self) -> Optional[str]:
        """Check if Conan is already installed and return version"""
        self.log_step("Checking existing Conan installation")
        
        try:
            returncode, stdout, stderr = self.run_command(['conan', '--version'], capture_output=True)
            if returncode == 0 and stdout.strip():
                version_parts = stdout.strip().split()
                if len(version_parts) >= 3:
                    version = version_parts[-1]
                    self.log_success(f"Conan {version} is already installed")
                    return version
                else:
                    self.log("Conan found but version format unexpected")
                    return None
            else:
                self.log("Conan not found, will install")
                return None
        except FileNotFoundError:
            self.log("Conan not found, will install")
            return None
    
    def install_conan(self) -> None:
        """Install Conan 2.x with pinned version"""
        self.log_step(f"Installing Conan {self.conan_version}")
        
        # Check if already installed with correct version
        existing_version = self.check_conan_installation()
        if existing_version and existing_version == self.conan_version:
            self.log_success(f"Conan {self.conan_version} already installed")
            return
        
        # Install Conan
        install_cmd = [sys.executable, '-m', 'pip', 'install', f'conan=={self.conan_version}']
        returncode, stdout, stderr = self.run_command(install_cmd)
        
        if returncode != 0:
            raise BootstrapError(f"Failed to install Conan: {stderr}")
        
        # Verify installation
        returncode, stdout, stderr = self.run_command(['conan', '--version'], capture_output=True)
        if returncode != 0:
            raise BootstrapError("Conan installation verification failed")
        
        if stdout.strip():
            version_parts = stdout.strip().split()
            if len(version_parts) >= 3:
                installed_version = version_parts[-1]
                if installed_version != self.conan_version:
                    raise BootstrapError(f"Version mismatch: expected {self.conan_version}, got {installed_version}")
                self.log_success(f"Conan {self.conan_version} installed successfully")
            else:
                self.log_success(f"Conan installed (version format unexpected)")
        else:
            self.log_success(f"Conan installed (version check skipped)")
    
    def configure_conan_remotes(self) -> None:
        """Configure Conan remotes"""
        self.log_step("Configuring Conan remotes")
        
        for name, url in self.remotes.items():
            # Check if remote already exists
            returncode, stdout, stderr = self.run_command(['conan', 'remote', 'list'], capture_output=True)
            if returncode == 0 and name in stdout:
                self.log(f"Remote '{name}' already configured")
                continue
            
            # Add remote
            cmd = ['conan', 'remote', 'add', name, url]
            returncode, stdout, stderr = self.run_command(cmd)
            if returncode != 0:
                self.log_warning(f"Failed to add remote '{name}': {stderr}")
            else:
                self.log_success(f"Added remote '{name}'")
    
    def detect_conan_profile(self) -> None:
        """Detect and create Conan profile"""
        self.log_step("Detecting Conan profile")
        
        cmd = ['conan', 'profile', 'detect', '--force']
        returncode, stdout, stderr = self.run_command(cmd)
        
        if returncode != 0:
            self.log_warning(f"Profile detection failed: {stderr}")
        else:
            self.log_success("Conan profile detected")
    
    def create_sparesparrow_directory(self) -> None:
        """Create sparesparrow directory structure"""
        self.log_step("Creating sparesparrow directory")
        
        if self.dry_run:
            self.log(f"Would create directory: {self.sparesparrow_dir}")
            return
        
        self.sparesparrow_dir.mkdir(exist_ok=True)
        self.log_success(f"Created directory: {self.sparesparrow_dir}")
    
    def clone_repository(self, name: str, url: str) -> None:
        """Clone a repository if it doesn't exist"""
        repo_dir = self.sparesparrow_dir / name
        
        if repo_dir.exists():
            self.log(f"Repository '{name}' already exists, skipping")
            return
        
        self.log(f"Cloning {name}...")
        cmd = ['git', 'clone', url, str(repo_dir)]
        returncode, stdout, stderr = self.run_command(cmd, cwd=self.sparesparrow_dir)
        
        if returncode != 0:
            raise BootstrapError(f"Failed to clone {name}: {stderr}")
        
        self.log_success(f"Cloned {name}")
    
    def clone_all_repositories(self) -> None:
        """Clone all OpenSSL repositories"""
        self.log_step("Cloning OpenSSL repositories")
        
        for name, url in self.repos.items():
            self.clone_repository(name, url)
    
    def install_extensions(self) -> None:
        """Install Conan extensions from openssl-tools"""
        self.log_step("Installing Conan extensions")
        
        openssl_tools_dir = self.sparesparrow_dir / 'openssl-tools'
        if not openssl_tools_dir.exists():
            raise BootstrapError("openssl-tools repository not found")
        
        # Create extensions directory
        if not self.dry_run:
            self.extensions_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy extensions
        extensions_source = openssl_tools_dir / 'extensions'
        if extensions_source.exists():
            if self.dry_run:
                self.log(f"Would copy extensions from {extensions_source} to {self.extensions_dir}")
            else:
                shutil.copytree(extensions_source, self.extensions_dir, dirs_exist_ok=True)
                self.log_success("Extensions installed")
        else:
            self.log_warning("Extensions directory not found in openssl-tools")
    
    def create_vscode_config(self) -> None:
        """Create VS Code configuration files"""
        self.log_step("Creating VS Code configuration")
        
        if not self.dry_run:
            self.vscode_dir.mkdir(exist_ok=True)
        
        # Extensions configuration
        extensions_config = {
            "recommendations": [
                "ms-vscode.cpptools",
                "ms-vscode.cmake-tools",
                "ms-python.python",
                "ms-vscode.vscode-json",
                "redhat.vscode-yaml",
                "github.vscode-pull-request-github",
                "ms-vscode.hexeditor"
            ]
        }
        
        extensions_file = self.vscode_dir / 'extensions.json'
        if self.dry_run:
            self.log(f"Would create {extensions_file}")
        else:
            with open(extensions_file, 'w') as f:
                json.dump(extensions_config, f, indent=2)
            self.log_success("Created extensions.json")
        
        # Settings configuration
        settings_config = {
            "C_Cpp.default.configurationProvider": "ms-vscode.cmake-tools",
            "C_Cpp.default.intelliSenseMode": "linux-gcc-x64",
            "cmake.configureOnOpen": True,
            "cmake.buildDirectory": "${workspaceFolder}/build",
            "files.associations": {
                "*.h": "c",
                "*.c": "c",
                "*.hpp": "cpp",
                "*.cpp": "cpp",
                "*.cc": "cpp",
                "*.cxx": "cpp"
            }
        }
        
        settings_file = self.vscode_dir / 'settings.json'
        if self.dry_run:
            self.log(f"Would create {settings_file}")
        else:
            with open(settings_file, 'w') as f:
                json.dump(settings_config, f, indent=2)
            self.log_success("Created settings.json")
        
        # Launch configuration
        launch_config = {
            "version": "0.2.0",
            "configurations": [
                {
                    "name": "Debug OpenSSL CLI",
                    "type": "cppdbg",
                    "request": "launch",
                    "program": "${workspaceFolder}/openssl/apps/openssl",
                    "args": ["version"],
                    "stopAtEntry": False,
                    "cwd": "${workspaceFolder}/openssl",
                    "environment": [],
                    "externalConsole": False,
                    "MIMode": "gdb",
                    "setupCommands": [
                        {
                            "description": "Enable pretty-printing for gdb",
                            "text": "-enable-pretty-printing",
                            "ignoreFailures": True
                        }
                    ]
                }
            ]
        }
        
        launch_file = self.vscode_dir / 'launch.json'
        if self.dry_run:
            self.log(f"Would create {launch_file}")
        else:
            with open(launch_file, 'w') as f:
                json.dump(launch_config, f, indent=2)
            self.log_success("Created launch.json")
    
    def validate_installation(self) -> None:
        """Validate the installation"""
        self.log_step("Validating installation")
        
        # Check Conan version
        returncode, stdout, stderr = self.run_command(['conan', '--version'], capture_output=True)
        if returncode != 0:
            raise BootstrapError("Conan validation failed")
        
        version = stdout.strip().split()[-1]
        if version != self.conan_version:
            raise BootstrapError(f"Version mismatch: expected {self.conan_version}, got {version}")
        
        self.log_success(f"Conan {version} validated")
        
        # Check remotes
        returncode, stdout, stderr = self.run_command(['conan', 'remote', 'list'], capture_output=True)
        if returncode == 0:
            for remote in self.remotes.keys():
                if remote in stdout:
                    self.log_success(f"Remote '{remote}' configured")
                else:
                    self.log_warning(f"Remote '{remote}' not found")
        
        # Check repositories
        for repo in self.repos.keys():
            repo_path = self.sparesparrow_dir / repo
            if repo_path.exists():
                self.log_success(f"Repository '{repo}' found")
            else:
                self.log_warning(f"Repository '{repo}' not found")
        
        # Check extensions
        if self.extensions_dir.exists():
            self.log_success("Extensions directory found")
        else:
            self.log_warning("Extensions directory not found")
    
    def run_minimal_mode(self) -> None:
        """Run minimal installation mode"""
        self.log(f"\n{Colors.BOLD}🚀 Starting minimal installation mode{Colors.END}")
        start_time = time.time()
        
        self.check_python_version()
        self.install_conan()
        self.configure_conan_remotes()
        self.detect_conan_profile()
        
        elapsed = time.time() - start_time
        self.log_success(f"Minimal installation completed in {elapsed:.1f} seconds")
    
    def run_full_mode(self) -> None:
        """Run full installation mode"""
        self.log(f"\n{Colors.BOLD}🚀 Starting full installation mode{Colors.END}")
        start_time = time.time()
        
        self.run_minimal_mode()
        self.create_sparesparrow_directory()
        self.clone_all_repositories()
        self.install_extensions()
        
        elapsed = time.time() - start_time
        self.log_success(f"Full installation completed in {elapsed:.1f} seconds")
    
    def run_dev_mode(self) -> None:
        """Run development installation mode"""
        self.log(f"\n{Colors.BOLD}🚀 Starting development installation mode{Colors.END}")
        start_time = time.time()
        
        self.run_full_mode()
        self.create_vscode_config()
        
        elapsed = time.time() - start_time
        self.log_success(f"Development installation completed in {elapsed:.1f} seconds")
    
    def run_validation_mode(self) -> None:
        """Run validation mode"""
        self.log(f"\n{Colors.BOLD}🔍 Validating existing installation{Colors.END}")
        
        try:
            self.validate_installation()
            self.log_success("Installation validation passed")
        except BootstrapError as e:
            self.log_error(f"Validation failed: {e}")
            sys.exit(1)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="OpenSSL Conan Development Environment Bootstrap Script",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python3 openssl-conan-init.py --minimal
    python3 openssl-conan-init.py --full --dry-run
    python3 openssl-conan-init.py --dev
    python3 openssl-conan-init.py --validate
        """
    )
    
    # Mode selection (mutually exclusive)
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument('--minimal', action='store_true', 
                           help='Install Conan 2.x and basic configuration (2-3 minutes)')
    mode_group.add_argument('--full', action='store_true',
                           help='Clone repositories and install extensions (8-12 minutes)')
    mode_group.add_argument('--dev', action='store_true',
                           help='Full setup with VS Code integration (12-15 minutes)')
    mode_group.add_argument('--validate', action='store_true',
                           help='Validate existing installation')
    
    # Options
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be done without making changes')
    parser.add_argument('--test-mode', action='store_true',
                       help='Run in test mode for CI validation')
    
    args = parser.parse_args()
    
    try:
        bootstrap = OpenSSLConanBootstrap(dry_run=args.dry_run, test_mode=args.test_mode)
        
        if args.validate:
            bootstrap.run_validation_mode()
        elif args.minimal:
            bootstrap.run_minimal_mode()
        elif args.full:
            bootstrap.run_full_mode()
        elif args.dev:
            bootstrap.run_dev_mode()
        
        if not args.dry_run and not args.test_mode:
            print(f"\n{Colors.BOLD}{Colors.GREEN}🎉 Bootstrap completed successfully!{Colors.END}")
            print(f"\nNext steps:")
            print(f"1. cd ~/sparesparrow/openssl")
            print(f"2. conan openssl:build --help")
            print(f"3. code . (if using --dev mode)")
        
    except BootstrapError as e:
        print(f"\n{Colors.RED}❌ Bootstrap failed: {e}{Colors.END}")
        sys.exit(1)
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}⚠️  Bootstrap interrupted by user{Colors.END}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.RED}❌ Unexpected error: {e}{Colors.END}")
        sys.exit(1)


if __name__ == '__main__':
    main()
