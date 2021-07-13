cmake_minimum_required(VERSION 3.12)

set(PROJECT "Foo")

PROJECT(${PROJECT})

# The version from the cmake settings
set(FOO_VERSION "undefined" CACHE STRING "FOO Library version")
# The dependency roots from cmake settings
set(POCO_ROOT_DIR CACHE FILEPATH "Path to the directory containing Poco .h/.lib/.dll/.so files")

if(MSVC)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /DWIN32 /EHsc /MP")
	set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} /MDd")
	set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} /MD")
endif(MSVC)

set(SOURCES
    src/foo_json.h
    src/foo_json.cpp
)

set(INCLUDE_FILES 
  src/foo_json.h
)

find_package(poco CONFIG)

add_library(${PROJECT} STATIC ${SOURCES})
target_compile_features(${PROJECT} PRIVATE cxx_std_17)
target_include_directories(${PROJECT} PRIVATE "${poco_INCLUDE_DIRS}")
target_include_directories(${PROJECT} INTERFACE $<INSTALL_INTERFACE:include>)
target_link_libraries(${PROJECT} "Poco::Poco")
target_compile_definitions(${PROJECT} PUBLIC POCO_STATIC)

# Generate the version file for use with find_package
configure_file(${CMAKE_SOURCE_DIR}/cmake/ConfigVersion.cmake.in "${CMAKE_CURRENT_BINARY_DIR}/cmake/ConfigVersion.cmake" @ONLY)

set(INCLUDE_INSTALL_DIR include)
set(LIB_INSTALL_DIR lib)
set(CURRENT_BUILD_DIR "${CMAKE_BINARY_DIR}")

# install the target and create export-set
install(TARGETS ${PROJECT}
    EXPORT ${PROJECT}Targets
    LIBRARY DESTINATION lib/$<CONFIGURATION>
    ARCHIVE DESTINATION lib/$<CONFIGURATION>
    RUNTIME DESTINATION lib/$<CONFIGURATION>
    INCLUDES DESTINATION include
)

# install the package header files 
install(FILES
        ${INCLUDE_FILES}
        DESTINATION include
)

# generate and install export file
install(EXPORT ${PROJECT}Targets
        FILE ${PROJECT}Targets.cmake
        NAMESPACE Foo::
        DESTINATION lib/cmake/Foo
)

# Helper macro for packaging
include(CMakePackageConfigHelpers)


set_property(TARGET ${PROJECT} PROPERTY VERSION ${FOO_VERSION})
set_property(TARGET ${PROJECT} PROPERTY SOVERSION 0)
set_property(TARGET ${PROJECT} PROPERTY INTERFACE_Foo_MAJOR_VERSION 0)
set_property(TARGET ${PROJECT} APPEND PROPERTY
  COMPATIBLE_INTERFACE_STRING Foo_MAJOR_VERSION
)

write_basic_package_version_file(
  "${CMAKE_CURRENT_BINARY_DIR}/FooConfigVersion.cmake"
  VERSION "${FOO_VERSION}"
  COMPATIBILITY AnyNewerVersion
)

# create config file
configure_package_config_file(${CMAKE_CURRENT_SOURCE_DIR}/cmake/Config.cmake.in
  "${CMAKE_CURRENT_BINARY_DIR}/FooConfig.cmake"
  INSTALL_DESTINATION lib/cmake/Foo
)

install(FILES
          "${CMAKE_CURRENT_BINARY_DIR}/${PROJECT}Config.cmake"
          "${CMAKE_CURRENT_BINARY_DIR}/${PROJECT}ConfigVersion.cmake"
        DESTINATION lib/cmake/Foo
)

# generate the export targets for the build tree
export(EXPORT ${PROJECT}Targets
       FILE "${CMAKE_CURRENT_BINARY_DIR}/cmake/${PROJECT}Targets.cmake"
       NAMESPACE MathFunctions::
)


