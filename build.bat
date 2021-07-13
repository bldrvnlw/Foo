conan install . Foo/0.2.0@ -s build_type=Release -s compiler.runtime=MD -o shared=False -s compiler="Visual Studio"
conan install . Foo/0.2.0@ -s build_type=Debug -s compiler.runtime=MDd -o shared=False -s compiler="Visual Studio"
:: Create a single multi-config package - no transitive dependencies
conan create . Foo/0.2.0@ -o shared=False -s build_type=Release
:: Create the individual dependency packages for the multi-package transitive requirementent retrieval in the CI
conan create . Foo_deps/0.2.0@ -o shared=False -s build_type=Release
conan create . Foo_deps/0.2.0@ -o shared=False -s build_type=Debug