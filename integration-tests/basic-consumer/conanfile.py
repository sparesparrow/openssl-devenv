from conan import ConanFile
from conan.tools.cmake import CMake, cmake_layout
from conan.tools.files import save
import os

class BasicConsumerConan(ConanFile):
    name = "basic-consumer"
    version = "1.0.0"
    settings = "os", "compiler", "build_type", "arch"
    generators = "CMakeDeps", "CMakeToolchain"
    
    def requirements(self):
        self.requires("openssl/4.0.0-dev@sparesparrow/stable")
    
    def layout(self):
        cmake_layout(self)
    
    def generate(self):
        self._generate_test_sources()
    
    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()
    
    def test(self):
        # Run the test executable
        test_exe = os.path.join(self.cpp.build.bindirs[0], "basic_consumer")
        if os.path.exists(test_exe):
            self.run(test_exe, cwd=self.build_folder)
        else:
            self.output.warn("Test executable not found")
    
    def _generate_test_sources(self):
        """Generate basic consumer test sources"""
        
        # CMakeLists.txt
        cmake_content = """
cmake_minimum_required(VERSION 3.15)
project(basic_consumer)

find_package(OpenSSL REQUIRED)

add_executable(basic_consumer main.cpp)
target_link_libraries(basic_consumer OpenSSL::SSL OpenSSL::Crypto)

# Test that we can find OpenSSL
message(STATUS "OpenSSL version: ${OpenSSL_VERSION}")
message(STATUS "OpenSSL shared: ${OpenSSL_SHARED}")
"""
        save(self, os.path.join(self.source_folder, "CMakeLists.txt"), cmake_content)
        
        # main.cpp
        main_content = """
#include <openssl/ssl.h>
#include <openssl/crypto.h>
#include <openssl/evp.h>
#include <iostream>

int main() {
    std::cout << "=== Basic OpenSSL Consumer Test ===" << std::endl;
    
    // Test basic functionality
    const char* version = OpenSSL_version(OPENSSL_VERSION);
    std::cout << "OpenSSL version: " << version << std::endl;
    
    // Test random number generation
    unsigned char random_bytes[16];
    if (RAND_bytes(random_bytes, sizeof(random_bytes)) == 1) {
        std::cout << "✓ Random number generation works" << std::endl;
    } else {
        std::cerr << "❌ Random number generation failed" << std::endl;
        return 1;
    }
    
    // Test hash computation
    EVP_MD_CTX* md_ctx = EVP_MD_CTX_new();
    if (md_ctx == nullptr) {
        std::cerr << "❌ Failed to create MD context" << std::endl;
        return 1;
    }
    
    const EVP_MD* md = EVP_sha256();
    if (EVP_DigestInit_ex(md_ctx, md, nullptr) <= 0) {
        std::cerr << "❌ Failed to initialize digest" << std::endl;
        EVP_MD_CTX_free(md_ctx);
        return 1;
    }
    
    const char* test_data = "Hello, OpenSSL Consumer!";
    if (EVP_DigestUpdate(md_ctx, test_data, strlen(test_data)) <= 0) {
        std::cerr << "❌ Failed to update digest" << std::endl;
        EVP_MD_CTX_free(md_ctx);
        return 1;
    }
    
    unsigned char hash[EVP_MAX_MD_SIZE];
    unsigned int hash_len;
    if (EVP_DigestFinal_ex(md_ctx, hash, &hash_len) <= 0) {
        std::cerr << "❌ Failed to finalize digest" << std::endl;
        EVP_MD_CTX_free(md_ctx);
        return 1;
    }
    
    EVP_MD_CTX_free(md_ctx);
    std::cout << "✓ SHA-256 hash computation works" << std::endl;
    
    std::cout << "\\n✅ Basic consumer test passed!" << std::endl;
    return 0;
}
"""
        save(self, os.path.join(self.source_folder, "main.cpp"), main_content)
