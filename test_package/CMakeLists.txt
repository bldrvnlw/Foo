cmake_minimum_required(VERSION 3.15)

# Set C++11 language standard
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

project(PackageTest CXX)

# CONAN_HDILIB_ROOT is from the cmake_paths generate conan_paths.cmake CMAKE_TOOLCHAIN_FILE
find_package(Foo PATHS ${CONAN_HDILIB_ROOT} CONFIG REQUIRED)
message("test_package list dir ${CMAKE_CURRENT_LIST_DIR}")

add_executable(example example.cpp)
target_link_libraries(example PRIVATE Foo)
message("FOO_INCLUDE_DIR: ${FOO_INCLUDE_DIR} ")
#target_include_directories(example PRIVATE ${FOO_INCLUDE_DIR})

install(TARGETS example
    RUNTIME DESTINATION bin)

add_custom_command(TARGET example POST_BUILD
	COMMAND "${CMAKE_COMMAND}"
	--install ${CMAKE_BINARY_DIR}
	--config $<CONFIGURATION>
	--prefix ${CMAKE_BINARY_DIR}
)