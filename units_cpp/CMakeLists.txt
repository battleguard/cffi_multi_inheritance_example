cmake_minimum_required(VERSION 3.12)

set(CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS ON)
project(units LANGUAGES CXX C VERSION 0.0.1)
add_library(units SHARED units.hpp units_c.cpp units.h)