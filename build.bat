conan install . Foo/0.2.0@ -s build_type=Release -s compiler.runtime=MD -o shared=False -s compiler="Visual Studio"
conan install . Foo/0.2.0@ -s build_type=Debug -s compiler.runtime=MDd -o shared=False -s compiler="Visual Studio"
:: Combined multi-config debug and release package 
conan create . Foo/0.2.0@ -o shared=False -s build_type=Release -s compiler.runtime=MD
:: deps package separate Debug & Release (this is dependant on Foo which has no build_type in the package_id)
conan create . Foo_deps/0.2.0@ -o shared=False -s build_type=Release -s compiler.runtime=MD
conan create . Foo_deps/0.2.0@ -o shared=False -s build_type=Debug -s compiler.runtime=MDd
