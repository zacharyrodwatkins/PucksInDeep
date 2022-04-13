#include <rclcpp>
#include <opencv2/core.hpp>
#include <opencv2/videoio.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc.hpp>
#include <iostream>
#include <stdio.h>
#include <ctime>
#include <chrono>
#include "tracker.hpp"
using namespace cv;
using namespace std;

// Get time stamp in microseconds.
uint64_t micros()
{
    uint64_t us = std::chrono::duration_cast<std::chrono::microseconds>(
            std::chrono::high_resolution_clock::now().time_since_epoch())
            .count();
    return us; 
}

int main(int, char**) { 
    tracker t = tracker();
    
    for(;;){
        t.process_frame();
        // t.show();
        t.tracker_write();
    }
}