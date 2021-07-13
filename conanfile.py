from conans import ConanFile
from conan.tools.cmake import CMakeDeps, CMake, CMakeToolchain
from pathlib import Path
import os
import subprocess

class FooConan(ConanFile):
    """Create a Foo or Foo_deps package

    Build one of two package names either:
    1.) Foo : builds a single multi-config CMake config-file package without dependencies
    2.) Foo_deps : building multiple single config conan compatible packages 
        that depends on multi-config Foo (as build_requirement) and contain Foo's dependencies
    """

    name = "Foo"
    default_version = "0.1"  # actual version supplied by the create command reference (e.g. conan create . Foo/m.n.o@)
    license = "MIT"
    default_name = "Foo"
    author = "B. van Lew"
    url = "github.com/bldrvnlw/Foo"
    description = "Combining multi-config with single config library packages"
    topics = ("example", "multi-config", "single config")
    settings = "os", "compiler", "build_type", "arch"
    options = {
            "shared": [False, None]} 
    generators = ("CMakeDeps")

    exports = "CMakeLists.txt", "src*", "cmake*", "*"

    def generate(self):
        print("In generate")
        tc = CMakeToolchain(self)
        tc.variables["FOO_VERSION"] = self.version
        if not self.name.endswith('_deps'):
            tc.variables["CMAKE_TOOLCHAIN_FILE"] = "conan_toolchain.cmake"
        tc.generate()
        deps = CMakeDeps(self)
        deps.generate()

    def set_name(self):
        self.name = self.name or self.default_name
        print(f"Set name to : {self.name}")
    
    def build_requirements(self):
        # The package is a build dependency of its corresponding _deps package
        if self.name.endswith('_deps'):
            print(f"Adding requirement: {self.default_name}/{self.version}")
            self.build_requires(f"{self.default_name}/{self.version}")

    def requirements(self):
        if self.settings.build_type == "None":
            print("Skip root package requirements for build_type NONE")
            return
        self.requires.add("poco/1.10.1")


    def _build_install(self, build_type):
        cmake = CMake(self) # , build_type=build_type
        # cmake.definitions["FOO_VERSION"] = self.version
        # cmake.definitions["POCO_ROOT_DIR"] = self.deps_cpp_info["poco"].rootpath
        # print(f"POCO root {self.deps_cpp_info['poco'].rootpath}")
        cmake.configure()
        try:
            cmake.install(build_type=build_type)
            print("Conan cmake build complete")
        except:
            print("Conan cmake build error")

    def _install(self, build_type, install_dir):
        print(f"Installing config {build_type} in {str(install_dir)}")
        result = None
        try:
            cmake = CMake(self)
            cmake.install(build_type=build_type)
            #result = subprocess.run(["cmake",
            #                "--install", self.build_folder,
            #                "--config", build_type,
            #                "--verbose",
            #                "--prefix", str(install_dir)],
            #                encoding='UTF-8')
            print("Install complete")

        except OSError as e:
            print(f"STDOUT \n {result.stdout}")
            print(f"STDERR \n {result.stderr}")
        
    def build(self):
        # Foo build_type Release builds Debug & Release
        # Foo build_type Debug depends on Foo build_type Release
        if not self.name.endswith('_deps'):
            install_dir = Path(self.build_folder).joinpath("install")
            install_dir.mkdir(exist_ok=True)
            print(f"Self build {self.settings.build_type}")
            self._build_install(self.settings.build_type)
            #self._install(self.settings.build_type, install_dir)
            # print(f"Self build Debug")
            # self._build("Debug")
            # self._install("Debug", install_dir)


    def package_id(self):
        print("In package_id")
        # remove build_type identification from the multi-config 
        # and the runtime on windows
        if not self.name.endswith('_deps'):
            del self.info.settings.build_type
            if self.settings.compiler == "Visual Studio":
                del self.info.settings.compiler.runtime

    def package(self):
        print("In package...")
        install_dir = Path(self.build_folder).joinpath("install")
        self.copy(pattern="*", src=str(install_dir))
        self.copy(pattern="*", src=str(install_dir))

    def package_info(self):
        if not self.name.endswith('_deps'):
            self.cpp_info.set_property("skip_deps_file", True)

