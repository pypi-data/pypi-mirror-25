cmake_minimum_required(VERSION 3.0)
project(example)

include_directories(${CMAKE_CURRENT_SOURCE_DIR}/../include)
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/include)
LINK_DIRECTORIES(${CMAKE_CURRENT_SOURCE_DIR}/../build)

add_subdirectory(pybind11)

add_library(pyDiamonds MODULE PyUniformPrior.cpp)
target_link_libraries(pyDiamonds PRIVATE pybind11::module)
target_link_libraries(pyDiamonds PRIVATE diamonds)
set_target_properties(pyDiamonds PROPERTIES PREFIX "${PYTHON_MODULE_PREFIX}"
        SUFFIX "${PYTHON_MODULE_EXTENSION}")