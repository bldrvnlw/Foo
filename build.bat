conan install . Foo/0.2.0@ -s build_type=Release -s compiler.runtime=MD -o shared=False -s compiler="Visual Studio"
conan install . Foo/0.2.0@ -s build_type=Debug -s compiler.runtime=MDd -o shared=False -s compiler="Visual Studio"
:: Combined multi-config debug and release package 
conan create . Foo/0.2.0@ -o shared=False -s build_type=Release -s compiler.runtime=MD
