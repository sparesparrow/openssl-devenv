from conan import ConanFile

class TestPackageConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "VirtualRunEnv"
    
    def requirements(self):
        self.requires(self.tested_reference_str)
    
    def test(self):
        # The test method is already in the main conanfile
        pass
