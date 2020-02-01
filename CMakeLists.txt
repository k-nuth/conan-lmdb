cmake_minimum_required (VERSION 3.4)
project (lmdb C CXX)

#TODO(fernando): use kthbuild 

if(EXISTS ${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
    include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
    conan_basic_setup()

    remove_definitions(-D_GLIBCXX_USE_CXX11_ABI=0)
    remove_definitions(-D_GLIBCXX_USE_CXX11_ABI=1)

    if ("${CMAKE_CXX_COMPILER_ID}" STREQUAL "GNU" OR "${CMAKE_CXX_COMPILER_ID}" MATCHES "Clang")
        if (NOT NOT_USE_CPP11_ABI)
            add_definitions(-D_GLIBCXX_USE_CXX11_ABI=1)
            message( STATUS "Knuth: Using _GLIBCXX_USE_CXX11_ABI=1")
        else()
            add_definitions(-D_GLIBCXX_USE_CXX11_ABI=0)
            message( STATUS "Knuth: Using _GLIBCXX_USE_CXX11_ABI=0")
        endif()
    endif()
else()
    message(WARNING "The file conanbuildinfo.cmake doesn't exist, you have to run conan install first")
endif()


option(ENABLE_SHARED "" OFF)
option(ENABLE_POSITION_INDEPENDENT_CODE "Enable POSITION_INDEPENDENT_CODE property" ON)

# ---------------------------------------------------------

set(MODE STATIC)
if (ENABLE_SHARED)
    set(MODE SHARED)
endif()


set (SOURCE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/lmdb/libraries/liblmdb")

set (SOURCE_FILES
    ${SOURCE_PATH}/mdb.c
    ${SOURCE_PATH}/lmdb.h
    ${SOURCE_PATH}/midl.h
    ${SOURCE_PATH}/midl.c
    # ${CMAKE_CURRENT_SOURCE_DIR}/mdb.def
)

set (CMAKE_DEBUG_POSTFIX "d")
set (EXECUTABLE_OUTPUT_PATH ${CMAKE_BINARY_DIR}/bin)
set (LIBRARY_OUTPUT_PATH  ${CMAKE_BINARY_DIR}/lib)
set_property (GLOBAL PROPERTY USE_FOLDERS ON)

# set (CMAKE_LINK_DEF_FILE_FLAG "/DEF:\"${CMAKE_CURRENT_SOURCE_DIR}/mdb.def\"")
add_library (lmdb ${SOURCE_FILES})


if (ENABLE_POSITION_INDEPENDENT_CODE)
    set_property(TARGET lmdb PROPERTY POSITION_INDEPENDENT_CODE ON)
endif(ENABLE_POSITION_INDEPENDENT_CODE)


if (WIN32)
    if (MSVC)
        include_directories (${CMAKE_CURRENT_SOURCE_DIR}/win32/stubs ${CMAKE_CURRENT_SOURCE_DIR}/win32/real)
    endif ()

    target_link_libraries (lmdb ntdll)
endif ()
