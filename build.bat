conan install . Foo/0.2.0@ -s build_type=Release -s compiler.runtime=MD -o shared=False -s compiler="Visual Studio"
conan install . Foo/0.2.0@ -s build_type=Debug -s compiler.runtime=MDd -o shared=False -s compiler="Visual Studio"
:: Create a single multi-config package - no transitive dependencies
:: conan create . Foo/0.2.0@ -o shared=False -s build_type=Release
:: Separate debg and release packages
conan create . Foo/0.2.0@ -o shared=False -s build_type=Release -s compiler.runtime=MD
conan create . Foo/0.2.0@ -o shared=False -s build_type=Debug -s compiler.runtime=MDd