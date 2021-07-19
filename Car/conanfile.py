from conans import ConanFile
from conan.tools.cmake import CMakeDeps, CMake, CMakeToolchain
from pathlib import Path


class CarConan(ConanFile):
    name = "Car"
    version = "0.1.0"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [False, None]}
    generators = ("CMakeDeps")
    requires = (
        "Foo_deps/0.2.0",
        "poco/1.9.4"
    )
    exports = "CMakeLists.txt", "*.cpp"

    def fix_config_packages(self):
        """ Iterate the dependencies and add the package root where
        it is marked as a "cmake_config_file" and when "skip_deps_file" is
        enabled. Permits using a package locak cmake config-file.
        """
        package_names = {r.ref.name for r in self.dependencies.host.values()}
        for package_name in package_names:
            cpp_info = self.dependencies[f"{package_name}"].new_cpp_info
            if (cpp_info.get_property("skip_deps_file", CMakeDeps) and
                    cpp_info.get_property("cmake_config_file", CMakeDeps)):
                package_root = Path(self.dependencies[
                    f"{package_name}"].package_folder)
                with open("conan_toolchain.cmake", "a") as toolchain:
                    toolchain.write(fr"""
set(CMAKE_MODULE_PATH "{package_root.as_posix()}" ${{CMAKE_MODULE_PATH}})
set(CMAKE_PREFIX_PATH "{package_root.as_posix()}" ${{CMAKE_PREFIX_PATH}})
                    """)

    def generate(self):
        print("In generate")
        tc = CMakeToolchain(self)
        tc.generate()
        deps = CMakeDeps(self)
        deps.generate()
        self.fix_config_packages()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()
