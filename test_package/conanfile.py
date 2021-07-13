import os
import platform
from conans import ConanFile, CMake, tools


class FooTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [False, None]}
    generators = "cmake_find_package_multi", "cmake_paths"

    def configure(self):
        print("In configure")

    def config_options(self):
        print("In config_options")

    def requirements(self):
        print("In requirements")

    def system_requirements(self):
        print("In system_requirements")

    def build(self):
        cmake = CMake(self)
        if self.settings.build_type == "None":
            print("Test consumption of HDILib in Release mode")
            self.settings.build_type = "Release"
            cmake = CMake(self, build_type="Release")
        print(f"")
        cmake.definitions["CMAKE_TOOLCHAIN_FILE"] = "conan_paths.cmake"
        cmake.configure()
        cmake.build()

    def imports(self):
        self.copy("*.dll", dst="bin", src="bin")
        self.copy("*.dylib*", dst="bin", src="lib")
        self.copy('*.so*', dst='bin', src='lib')

    def test(self):
        if not tools.cross_building(self.settings):
            os.chdir("bin")
            if platform.system() == 'Windows':
                examplePath = Path("./", str(self.build_folder), "bin", "example.exe")
                self.run(f"{str(examplePath)}")
            else:
                self.run(".%sexample" % os.sep)
