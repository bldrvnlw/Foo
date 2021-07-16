cmake_minimum_required(VERSION 3.15)

# Set C++11 language standard
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

project(PackageTest CXX)

# CONAN_HDILIB_ROOT is from the cmake_paths generate conan_paths.cmake CMAKE_TOOLCHAIN_FILE
find_package(Foo CONFIG REQUIRED)
find_package(poco CONFIG REQUIRED)

add_executable(example example.cpp)
target_include_directories(example PRIVATE ${FOO_INCLUDE_DIR})
target_link_libraries(example PRIVATE Foo::Foo)
target_link_libraries(example PRIVATE Poco::Poco)

install(TARGETS example
    RUNTIME DESTINATION bin)

add_custom_command(TARGET example POST_BUILD
	COMMAND "${CMAKE_COMMAND}"
	--install ${CMAKE_BINARY_DIR}
	--config $<CONFIGURATION>
	--prefix ${CMAKE_BINARY_DIR}
)