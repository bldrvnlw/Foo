## Dummy repo for conan testing

This demonstrates using conan to create the following:


*a. **A conan dependency free** multi configuration (Debug/Release)config-file package: **Foo***
*b. Two conan packages (Debug/Release) that contain the conan dependencies and have a dependency on **Foo** but are otherwise empty: **Foo_deps***


The conan dependency tree is as follows:

```
  Foo_deps (Release) ---> Foo (Release/Debug)
                     ---> poco (Release) ---> various transitive deps

  Foo_deps (Debug)   ---> Foo (Release/Debug)
                     ---> poco (Debug) ---> various transitive deps

Legend:
    conan requirements dependency arrow: --->
```

### Example contents

1. Contains Foo - a static lib package with a dependency on Poco
    * single example function do_the_foo
    * builds conan package containing cmake config-file package
    * package contains debug and release .lib and corresponding include
    * depends on poco 1.9.4
    * conan test_package

2. Contains Bar - conan free build, dependant on Foo.
3. Contains Car - conan driven build, dependant on Foo_deps and by extension Foo.

### Building the example

For the top level **Foo** and **Foo_deps** see build.bat for a sequence of Windows commands.

### Building the consumer examples (Br & Car)

See the README.md for those examples.

### Notes

1. The name of the package **Foo** or **Foo_deps** mut be provided at build time (see build.bat)
2. Although built with conan the items requires and full_require in conaninfo.txt are deliberately made empty.