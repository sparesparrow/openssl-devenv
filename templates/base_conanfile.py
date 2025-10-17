#!/usr/bin/env python3
"""
Base Conan Package Template with User/Channel Support
Provides foundation for OpenSSL layered architecture packages
"""

import os
import re
from conan import ConanFile
from conan.errors import ConanInvalidConfiguration


class BaseOpenSSLConan(ConanFile):
    """
    Base class for OpenSSL Conan packages with user/channel support

    Features:
    - User/channel reference support via environment variables
    - Version detection and validation
    - Common package metadata
    - Environment-specific configuration
    """

    # Default user/channel - can be overridden via environment variables
    default_user = "sparesparrow"
    default_channel = "stable"

    def init(self):
        """Initialize package with user/channel support"""
        # Get user/channel from environment or use defaults
        self.user = os.getenv("CONAN_USER", self.default_user)
        self.channel = os.getenv("CONAN_CHANNEL", self.default_channel)

        # Validate user/channel format
        self._validate_user_channel()

        # Set package reference
        self.reference = f"{self.user}/{self.channel}"

        self.output.info(f"Package reference: {self.name}/{self.version}@{self.reference}")

    def _validate_user_channel(self):
        """Validate user and channel names"""
        # User validation: alphanumeric, hyphen, underscore
        user_pattern = r'^[a-zA-Z0-9_-]+$'
        if not re.match(user_pattern, self.user):
            raise ConanInvalidConfiguration(f"Invalid user name: {self.user}. Must match {user_pattern}")

        # Channel validation: alphanumeric, hyphen, underscore, dot
        channel_pattern = r'^[a-zA-Z0-9_.-]+$'
        if not re.match(channel_pattern, self.channel):
            raise ConanInvalidConfiguration(f"Invalid channel name: {self.channel}. Must match {channel_pattern}")

    @property
    def package_reference(self):
        """Get full package reference"""
        return f"{self.name}/{self.version}@{self.user}/{self.channel}"

    def get_version_info(self):
        """Get version information with channel context"""
        version_info = {
            "version": self.version,
            "user": self.user,
            "channel": self.channel,
            "reference": self.package_reference,
            "is_stable": self.channel == "stable",
            "is_dev": "dev" in self.channel.lower(),
            "is_testing": "test" in self.channel.lower() or self.channel == "testing"
        }
        return version_info

    def configure(self):
        """Base configure method - can be extended by subclasses"""
        # Set common configuration based on channel
        if hasattr(self, 'settings'):
            # Configure based on channel type
            if self.channel == "dev":
                # Development builds may have different settings
                pass
            elif self.channel == "testing":
                # Testing builds may enable additional validation
                pass
            elif self.channel == "stable":
                # Stable builds use production settings
                pass

    def validate(self):
        """Base validation - can be extended by subclasses"""
        # Common validation logic
        version_info = self.get_version_info()

        # Validate version format for stable channel
        if version_info["is_stable"]:
            # Stable versions should follow semantic versioning
            semver_pattern = r'^\d+\.\d+\.\d+(-[a-zA-Z0-9.-]+)?(\+[a-zA-Z0-9.-]+)?$'
            if not re.match(semver_pattern, self.version):
                raise ConanInvalidConfiguration(
                    f"Stable channel requires semantic version (x.y.z), got: {self.version}"
                )

    def export(self):
        """Export phase - set package metadata"""
        # Export version info for consumers
        version_info = self.get_version_info()
        self.output.info(f"Exporting package: {version_info['reference']}")

    def package_info(self):
        """Base package info - can be extended by subclasses"""
        # Add common environment variables
        version_info = self.get_version_info()
        self.runenv_info.define("PACKAGE_USER", version_info["user"])
        self.runenv_info.define("PACKAGE_CHANNEL", version_info["channel"])
        self.runenv_info.define("PACKAGE_REFERENCE", version_info["reference"])

        # Add channel-specific environment variables
        if version_info["is_dev"]:
            self.runenv_info.define("PACKAGE_IS_DEV", "true")
        if version_info["is_testing"]:
            self.runenv_info.define("PACKAGE_IS_TESTING", "true")
        if version_info["is_stable"]:
            self.runenv_info.define("PACKAGE_IS_STABLE", "true")


class OpenSSLFoundationConan(BaseOpenSSLConan):
    """
    Base class for foundation layer packages
    (openssl-base, openssl-fips-data)
    """

    package_type = "header-library"
    settings = None

    def package_info(self):
        super().package_info()
        # Foundation packages typically don't provide libs/binaries
        self.cpp_info.bindirs = []
        self.cpp_info.libdirs = []


class OpenSSLToolingConan(BaseOpenSSLConan):
    """
    Base class for tooling layer packages
    (openssl-tools)
    """

    package_type = "python-require"
    settings = "os", "arch", "compiler", "build_type"


class OpenSSLDomainConan(BaseOpenSSLConan):
    """
    Base class for domain layer packages
    (openssl)
    """

    package_type = "library"
    settings = "os", "compiler", "build_type", "arch"

    options = {
        "shared": [True, False],
        "fPIC": [True, False],
    }

    default_options = {
        "shared": True,
        "fPIC": True,
    }

    def configure(self):
        super().configure()
        # Static builds need fPIC
        if not self.options.shared:
            self.options.fPIC = True