cmake_minimum_required(VERSION 3.0)
project(sysrepo-plugin-system C)

include_directories(
    ${CMAKE_SOURCE_DIR}/src
)

set(
    SOURCES
    
    src/plugin.c

    # startup
    src/plugin/startup/load.c
    src/plugin/startup/store.c

    # ly_tree
    src/plugin/ly_tree.c

    # subs
    src/plugin/subscription/change.c
    src/plugin/subscription/operational.c
    src/plugin/subscription/rpc.c
)

set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${CMAKE_SOURCE_DIR}/CMakeModules")
find_package(SYSREPO REQUIRED)
find_package(LIBYANG REQUIRED)
find_package(SRPC REQUIRED)
find_package(LIBSYSTEMD)
find_package(AUGYANG)

add_library(
    ${PROJECT_NAME}
    ${SOURCES}
)

target_link_libraries(
    ${PROJECT_NAME}
    ${SYSREPO_LIBRARIES}
    ${LIBYANG_LIBRARIES}
    ${SRPC_LIBRARIES}
)

include_directories(
    ${SYSREPO_INCLUDE_DIRS}
    ${LIBYANG_INCLUDE_DIRS}
    ${SRPC_INCLUDE_DIRS}
)

# augyang support
if(AUGYANG_FOUND)
    add_compile_definitions(AUGYANG)
else(AUGYANG_FOUND)
    message(WARNING "AUGYANG not found - augeas support will be disabled")
endif()