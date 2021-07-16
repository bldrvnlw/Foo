cmake_minimum_required(VERSION 3.15)
project(Bar CXX)

# Get FindPoco to facilitate the build and tweak it for the poco build this demo is using
file(MAKE_DIRECTORY "${CMAKE_CURRENT_LIST_DIR}/cmake")
file(DOWNLOAD https://raw.githubusercontent.com/astahl/poco-cmake/master/cmake/FindPoco.cmake ${CMAKE_CURRENT_LIST_DIR}/cmake/FindPoco.cmake)
file(READ ${CMAKE_CURRENT_LIST_DIR}/cmake/FindPoco.cmake FIND_POCO)
string(REPLACE ".dll" "md.lib" FIND_POCO  "${FIND_POCO}")
string(REPLACE "NAMES Poco\${component}" "NAMES Poco\${component}md" FIND_POCO  "${FIND_POCO}")
file(WRITE ${CMAKE_CURRENT_LIST_DIR}/cmake/FindPoco.cmake "${FIND_POCO}")
list(APPEND CMAKE_MODULE_PATH ${CMAKE_CURRENT_LIST_DIR}/cmake )

# Set C++11 language standard
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(Foo_ROOT "" CACHE FILEPATH "path to Foo root")
set(Poco_DIR "" CACHE FILEPATH "root path for Poco (used by FindPoco.cmake)")

# CONAN_HDILIB_ROOT is from the cmake_paths generate conan_paths.cmake CMAKE_TOOLCHAIN_FILE
find_package(Foo 0.2.0 CONFIG REQUIRED)
find_package(Poco REQUIRED JSON)

add_executable(Bar bar.cpp)
target_include_directories(Bar PRIVATE ${FOO_INCLUDE_DIR})

target_link_libraries(Bar PRIVATE Foo::Foo)
target_link_libraries(Bar PRIVATE ${Poco_Foundation_LIBRARY};${Poco_Util_LIBRARY};${Poco_JSON_LIBRARY})
