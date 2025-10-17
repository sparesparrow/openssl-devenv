from conan import ConanFile

class TestPackageReuseConan(ConanFile):
    name = "test-package-reuse"
    version = "1.0.0"
    description = "Test package to verify OpenSSL ecosystem package reuse"
    
    settings = "os", "compiler", "build_type", "arch"
    
    def requirements(self):
        # Test foundation layer packages
        self.requires("openssl-base/1.0.0")
        self.requires("openssl-fips-data/140-3.1")
        self.requires("openssl-tools/1.0.0")
    
    # def build_requirements(self):
    #     # Test toolchain package (requires ARM target)
    #     self.tool_requires("arm-toolchain/13.2")
    
    def test(self):
        # Test that packages are properly available
        self.output.info("Testing package reuse...")
        
        # Test openssl-base
        openssl_base = self.dependencies["openssl-base"]
        self.output.info(f"✅ openssl-base version: {openssl_base.ref.version}")
        
        # Test openssl-fips-data
        fips_data = self.dependencies["openssl-fips-data"]
        self.output.info(f"✅ openssl-fips-data version: {fips_data.ref.version}")
        
        # Test openssl-tools
        tools = self.dependencies["openssl-tools"]
        self.output.info(f"✅ openssl-tools version: {tools.ref.version}")
        
        # Test arm-toolchain (commented out - requires ARM target)
        # toolchain = self.dependencies.build["arm-toolchain"]
        # self.output.info(f"✅ arm-toolchain version: {toolchain.ref.version}")
        
        self.output.info("🎉 All packages successfully reused from Cloudsmith!")
