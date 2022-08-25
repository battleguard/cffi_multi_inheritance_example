cmake_minimum_required(VERSION 3.12)

set (CMAKE_CXX_STANDARD 11)
set(CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS ON)
project(units LANGUAGES CXX C VERSION 0.0.1)
add_library(units SHARED units.hpp units_c.cpp units.h)
set_target_properties(units PROPERTIES PUBLIC_HEADER units.h)


set(CMAKE_INSTALL_PREFIX "${CMAKE_BINARY_DIR}/../units_install" CACHE PATH "Installation path" FORCE)
install(TARGETS units
   RUNTIME DESTINATION  bin
   PUBLIC_HEADER DESTINATION  include/units
)
