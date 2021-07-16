## Build without conan

Anexample of a desktop developer working without conan and potentially buildingdependencies

- Get prebuilt Foo 0.2.0 and unpack
- Get poco 1.9.4 and either build or unpack (in this demo the conan center prebuilt poco is reused)
- Run cmake gui to generate supply the dependency paths
    - Set Foo_ROOT to the root of Foo 0.2.0
    - Set Poco_DIR to the root of poco 1.9.4
- cmake generate
- cmake configure
- Build using VS