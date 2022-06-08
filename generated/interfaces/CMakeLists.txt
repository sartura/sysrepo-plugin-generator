cmake_minimum_required(VERSION 3.0)
project(sysrepo-plugin-interfaces C)

include_directories(
    ${CMAKE_SOURCE_DIR}
)

set(
    SOURCES
    
    main.c
    plugin.c

    # startup
    plugin/startup/load.c
    plugin/startup/store.c

    # subs
    plugin/subscription/change.c
    plugin/subscription/operational.c
    plugin/subscription/rpc.c
)

set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${CMAKE_SOURCE_DIR}/CMakeModules")
find_package(SYSREPO REQUIRED)
find_package(LIBYANG REQUIRED)
find_package(SRPC REQUIRED)
find_package(LIBSYSTEMD)
find_package(AUGYANG)

add_executable(
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