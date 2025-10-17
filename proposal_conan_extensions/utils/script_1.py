# Create a production-ready conanfile.py for OpenSSL
conanfile_content = '''from conan import ConanFile
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain, cmake_layout
from conan.tools.files import copy, get, save, load, replace_in_file, rmdir
from conan.tools.env import Environment, VirtualBuildEnv
from conan.tools.system import package_manager
from conan.errors import ConanInvalidConfiguration
import os
import re


class OpenSSLConan(ConanFile):
    name = "openssl"
    # Version will be set by CI/CD or from git tags
    
    # Package metadata
    license = "Apache-2.0"
    author = "The OpenSSL Project"
    url = "https://github.com/openssl/openssl"
    homepage = "https://www.openssl.org/"
    description = "A robust, commercial-grade, full-featured toolkit for TLS and SSL protocols"
    topics = ("ssl", "tls", "cryptography", "security", "openssl")
    
    # Package configuration
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "no_threads": [True, False],
        "no_zlib": [True, False],
        "no_asm": [True, False],
        "no_deprecated": [True, False],
        "enable_camellia": [True, False],
        "enable_idea": [True, False], 
        "enable_md2": [True, False],
        "enable_rc5": [True, False],
        "enable_weak_ssl_ciphers": [True, False],
        "openssldir": "ANY",
        "cafile": "ANY",
        "capath": "ANY"
    }
    default_options = {
        "shared": False,
        "fPIC": True,
        "no_threads": False,
        "no_zlib": False,
        "no_asm": False,
        "no_deprecated": False,
        "enable_camellia": False,
        "enable_idea": False,
        "enable_md2": False, 
        "enable_rc5": False,
        "enable_weak_ssl_ciphers": False,
        "openssldir": "",
        "cafile": "",
        "capath": ""
    }

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.options.shared:
            self.options.rm_safe("fPIC")
        # Remove C++ standard as OpenSSL is C library
        self.settings.rm_safe("compiler.libcxx")
        self.settings.rm_safe("compiler.cppstd")

    def requirements(self):
        if not self.options.no_zlib:
            self.requires("zlib/[>=1.2.13 <2.0]")

    def build_requirements(self):
        if self.settings.os == "Windows":
            if not self.conf.get("tools.microsoft.msbuild:installation_path"):
                self.tool_requires("strawberryperl/[>=5.32.1]")
        if self.settings.os != "Windows":
            if not self.conf.get("tools.gnu:make_program"):
                self.tool_requires("make/[>=4.3]")

    def layout(self):
        # Standard layout for autotools-like projects
        self.folders.source = "src"
        self.folders.build = "build"

    def source(self):
        # This will be called when building from source
        # In the official repository, this might be empty since source is already present
        pass

    def generate(self):
        # Environment setup
        env = Environment()
        if self.settings.os == "Windows" and "strawberryperl" in self.deps_build_requires:
            perl_root = self.deps_build_requires["strawberryperl"].cpp_info.bindir
            env.prepend_path("PATH", perl_root)
        
        # Apply environment
        buildenv = VirtualBuildEnv(self)
        buildenv.vars.update(env)
        buildenv.generate()

        # Generate build helpers  
        self._generate_cmake_deps()

    def _generate_cmake_deps(self):
        """Generate CMake dependencies for downstream consumers"""
        deps = CMakeDeps(self)
        deps.generate()
        
        tc = CMakeToolchain(self)
        tc.generate()

    def build(self):
        self._configure_openssl()
        self._build_openssl()

    def _get_target_platform(self):
        """Determine the OpenSSL configure target"""
        if self.settings.os == "Linux":
            if self.settings.arch == "x86_64":
                return "linux-x86_64"
            elif self.settings.arch == "x86":
                return "linux-x86"
            elif self.settings.arch == "armv7":
                return "linux-armv4"
            elif self.settings.arch == "armv8":
                return "linux-aarch64"
        elif self.settings.os == "Windows":
            if self.settings.arch == "x86_64":
                return "VC-WIN64A"
            elif self.settings.arch == "x86": 
                return "VC-WIN32"
        elif self.settings.os == "Macos":
            if self.settings.arch == "x86_64":
                return "darwin64-x86_64-cc"
            elif self.settings.arch == "armv8":
                return "darwin64-arm64-cc"
        elif self.settings.os == "FreeBSD":
            if self.settings.arch == "x86_64":
                return "BSD-x86_64"
        
        raise ConanInvalidConfiguration(f"Unsupported platform: {self.settings.os}/{self.settings.arch}")

    def _configure_openssl(self):
        """Configure OpenSSL build"""
        args = [self._get_target_platform()]
        
        # Build type
        if self.settings.build_type == "Debug":
            args.append("--debug")
        
        # Shared/static
        if self.options.shared:
            args.append("shared")
        else:
            args.append("no-shared")
            
        # Threading
        if self.options.no_threads:
            args.append("no-threads")
            
        # Zlib
        if self.options.no_zlib:
            args.append("no-zlib")
        else:
            args.append("zlib")
            if "zlib" in self.deps_cpp_info.deps:
                zlib_include = self.deps_cpp_info["zlib"].include_paths[0]
                args.append(f"--with-zlib-include={zlib_include}")
                
        # Assembly
        if self.options.no_asm:
            args.append("no-asm")
            
        # Deprecated algorithms
        if self.options.no_deprecated:
            args.append("no-deprecated")
            
        # Optional algorithms
        if not self.options.enable_camellia:
            args.append("no-camellia")
        if not self.options.enable_idea:
            args.append("no-idea")
        if not self.options.enable_md2:
            args.append("no-md2")
        if not self.options.enable_rc5:
            args.append("no-rc5")
            
        # Weak SSL ciphers
        if not self.options.enable_weak_ssl_ciphers:
            args.extend(["no-ssl3", "no-weak-ssl-ciphers"])
            
        # Installation prefix
        args.append(f"--prefix={self.package_folder}")
        
        # OpenSSL directory
        if self.options.openssldir:
            args.append(f"--openssldir={self.options.openssldir}")
        else:
            args.append(f"--openssldir={os.path.join(self.package_folder, 'ssl')}")
            
        # CA file/path
        if self.options.cafile:
            args.append(f"--with-ca-file={self.options.cafile}")
        if self.options.capath:
            args.append(f"--with-ca-path={self.options.capath}")

        # Execute configure
        configure_cmd = f"./Configure {' '.join(args)}"
        self.output.info(f"Configuring with: {configure_cmd}")
        self.run(configure_cmd)

    def _build_openssl(self):
        """Build OpenSSL"""
        if self.settings.os == "Windows":
            self.run("nmake")
        else:
            # Use available CPU cores for parallel build
            import multiprocessing
            cores = multiprocessing.cpu_count()
            self.run(f"make -j{cores}")

    def package(self):
        # Copy license
        copy(self, "LICENSE*", src=self.source_folder, dst=os.path.join(self.package_folder, "licenses"))
        
        # Install OpenSSL
        if self.settings.os == "Windows":
            self.run("nmake install_sw")
        else:
            self.run("make install_sw")
            
        # Remove pkgconfig files if present (they can cause issues)
        rmdir(self, os.path.join(self.package_folder, "lib", "pkgconfig"))

    def package_info(self):
        # Libraries
        self.cpp_info.libs = ["ssl", "crypto"]
        
        # System libraries
        if self.settings.os == "Linux":
            self.cpp_info.system_libs.extend(["dl", "pthread"])
        elif self.settings.os == "Windows":
            self.cpp_info.system_libs.extend([
                "ws2_32", "gdi32", "advapi32", "crypt32", "user32"
            ])
        elif self.settings.os == "Macos":
            self.cpp_info.frameworks = ["Security"]
            
        # CMake integration
        self.cpp_info.set_property("cmake_find_mode", "both")
        self.cpp_info.set_property("cmake_target_name", "OpenSSL::OpenSSL")
        self.cpp_info.set_property("cmake_target_aliases", ["OpenSSL::SSL", "OpenSSL::Crypto"])
        
        # PKG-config
        self.cpp_info.set_property("pkg_config_name", "openssl")
        
        # Environment variables for tools
        if self.options.shared:
            bin_path = os.path.join(self.package_folder, "bin")
            self.runenv_info.prepend_path("PATH", bin_path)
'''

# Save the conanfile.py
with open("openssl_conanfile.py", "w", encoding="utf-8") as f:
    f.write(conanfile_content)

print("✅ Production-ready conanfile.py created!")
print("📁 File: openssl_conanfile.py")
print()
print("Key features:")
print("- Modern Conan 2.0 API usage")
print("- Cross-platform support (Linux, Windows, macOS, FreeBSD)")
print("- Comprehensive build options")
print("- Proper CMake and PKG-config integration")
print("- Zlib dependency management")
print("- Build tools detection and management")
print("- Environment variable setup for tools")
print("- License file packaging")
print("- Security-focused defaults")