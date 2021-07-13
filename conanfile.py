from conans import ConanFile
from conan.tools.cmake import CMakeDeps, CMake, CMakeToolchain
from pathlib import Path

class FooConan(ConanFile):
    """Create a Foo or Foo_deps package

    Build one of two package names either:
    1.) Foo : builds a single multi-config CMake config-file package without dependencies
    2.) Foo_deps : building multiple single config conan compatible packages 
        that depends on multi-config Foo (as build_requirement) and contain Foo's dependencies
    """

    # name = "Foo" pass either Foo or Foo_deps as name
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

    def requirements(self):
        if self.name.endswith('_deps'):
            print(f"Adding requirement: {self.default_name}/{self.version}")
            self.requires.add(f"{self.default_name}/{self.version}")

        self.requires.add("poco/1.10.1")


    def _build_install(self, build_type):
        cmake = CMake(self) 
        cmake.configure()
        try:
            cmake.install(build_type=build_type)
            print("Conan cmake build complete")
        except:
            print("Conan cmake build error")
        
    def build(self):
        # Build Debug and Release
        if not self.name.endswith('_deps'):
            install_dir = Path(self.build_folder).joinpath("install")
            install_dir.mkdir(exist_ok=True)
            print(f"Self build {self.settings.build_type}")
            if self.settings.compiler == "Visual Studio":
                self.settings.compiler.runtime="MD"
            self._build_install("Release")
            if self.settings.compiler == "Visual Studio":
                self.settings.compiler.runtime="MDd"
            self._build_install("Debug")


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

