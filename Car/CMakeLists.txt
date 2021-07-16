cmake_minimum_required(VERSION 3.15)
project(Car CXX)

find_package(Foo 0.2.0 CONFIG REQUIRED)
find_package(Poco REQUIRED)

add_executable(Car car.cpp)
target_include_directories(Car PRIVATE ${FOO_INCLUDE_DIR})

target_link_libraries(Car PRIVATE Foo::Foo)
target_link_libraries(Car PRIVATE Poco::Poco)
