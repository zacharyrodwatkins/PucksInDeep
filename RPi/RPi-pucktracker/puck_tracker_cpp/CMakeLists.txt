cmake_minimum_required(VERSION 2.8)
project( PuckTrackerCpp )
find_package( OpenCV REQUIRED )
include_directories( ${OpenCV_INCLUDE_DIRS} )
include_directories(lib/PuckTracker)
add_library(tracker SHARED
    lib/PuckTracker/tracker.cpp
    lib/PuckTracker/tracker.hpp
)

add_library(savgol SHARED
    lib/savgol/savgol.hpp
)

add_executable( puck_tracker puck_tracker.cpp lib/PuckTracker/tracker.cpp  lib/savgol.cpp)

target_link_libraries( puck_tracker ${OpenCV_LIBS} )

# link_directories(tracker)
# add_subdirectory(tracker)

# add_executable( ${PROJECT_NAME} ${SOURCE_FILES} )

#and here
# target_link_libraries( ${PROJECT_NAME} tracker )