cmake_minimum_required(VERSION 3.5)
project(pt)

find_package( OpenCV REQUIRED )
include_directories( ${OpenCV_INCLUDE_DIRS} )

include_directories(src/lib/Savgol src/lib/PuckTracker)


# add_library(savgol SHARED
#     src/lib/savgol/savgol.hpp
#     src/lib/savgol/savgol.cpp

# )
# add_library(tracker SHARED
#     src/lib/PuckTracker/tracker.cpp
#     src/lib/PuckTracker/tracker.hpp
#     src/lib/savgol/savgol.hpp
#     src/lib/savgol/savgol.cpp
# )

# Default to C99
if(NOT CMAKE_C_STANDARD)
  set(CMAKE_C_STANDARD 99)
endif()

# Default to C++14
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 14)
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
# uncomment the following section in order to fill in
# further dependencies manually.
# find_package(<dependency> REQUIRED)
find_package(rclcpp REQUIRED)
find_package(hockey_msgs REQUIRED)

add_executable(puck_tracker src/puck_tracker.cpp
 src/lib/PuckTracker/tracker.cpp src/lib/savgol/savgol.cpp)
ament_target_dependencies(puck_tracker rclcpp hockey_msgs)


target_link_libraries( puck_tracker ${OpenCV_LIBS} )

install(TARGETS
  puck_tracker
  DESTINATION lib/${PROJECT_NAME})

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # uncomment the line when a copyright and license is not present in all source files
  #set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # uncomment the line when this package is not in a git repo
  #set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
