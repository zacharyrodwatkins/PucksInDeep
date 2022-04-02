cmake_minimum_required(VERSION 2.8)
project( SavgolCpp )
include_directories(lib)

add_library(savgol SHARED lib/savgol.cpp lib/savgol.hpp)

add_executable(main main.cpp lib/savgol.cpp)
