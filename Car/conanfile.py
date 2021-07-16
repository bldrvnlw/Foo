from conans import ConanFile
from conan.tools.cmake import CMakeDeps, CMake, CMakeToolchain
from conans.client.output import ConanOutput
from conans.client.command import Command
from conans.client.conan_api import Conan
from six import StringIO
import re


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

    def _get_package_path(self, package_str):
        stream = StringIO()
        output = ConanOutput(stream)
        conan_api = Conan(output=output)
        command = Command(conan_api)
        command.run(["info", f"{package_str}@", "--paths"])
        outstr = stream.getvalue()
        package_path = package_str.replace("/", r"\\")
        pat = re.compile(fr"\n[ ]*package_folder: (.*{package_path}.*)\n")   # group capture raw string preserve \\
        x = pat.search(outstr)  # first occurrence
        package_root = x.groups()[0]  # e.g. 'C:\\Users\\bvanlew\\.conan\\data\\Foo\\0.2.0\\_\\_\\package\\f34583babc53eea864e76087e72c782c95f0f402'
        return package_root.replace("\\", "/")

    def _inject_package_root(self, package_str):
        package_root = self._get_package_path(package_str)
        with open("conan_toolchain.cmake", "a") as toolchain:
            toolchain.write(fr"""
set(CMAKE_MODULE_PATH "{package_root}" ${{CMAKE_MODULE_PATH}})
set(CMAKE_PREFIX_PATH "{package_root}" ${{CMAKE_PREFIX_PATH}})
            """)

    def generate(self):
        print("In generate")
        tc = CMakeToolchain(self)
        tc.generate()
        deps = CMakeDeps(self)
        deps.generate()
        self._inject_package_root(r"Foo/0.2.0")

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()
