#include <opencv2/core.hpp>
#include <opencv2/videoio.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc.hpp>
#include <iostream>
#include <stdio.h>
#include <ctime>
#include <chrono>
#include "tracker.hpp"
#include "rclcpp/rclcpp.hpp"
#include "hockey_msgs/msg/puck_status.hpp"

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

class TrackerNode : public rclcpp::Node
{

private:
    rclcpp::Publisher<hockey_msgs::msg::PuckStatus>::SharedPtr puck_publisher_;
    tracker t = tracker();
    hockey_msgs::msg::PuckStatus puck_msg;

public:
    TrackerNode()
        : Node("puck_tracker")
    {
        // ros stuff
        puck_publisher_ = this->create_publisher<hockey_msgs::msg::PuckStatus>("PUCK", 1);
        puck_msg = hockey_msgs::msg::PuckStatus();

    }

    int run(void)
    {
        t.process_frame();
        this->publish();
        t.show();
        // t.writeVideo();
        return 0;
    }



    void publish(void){
        puck_msg.x = t.x;
        puck_msg.y = t.y;
        puck_msg.x_vel = t.vx;
        puck_msg.y_vel = t.vy;
        puck_publisher_->publish(puck_msg);
    }
};

int main(int argc, char *argv[])
{
    rclcpp::init(argc, argv);
    shared_ptr<TrackerNode> tnode_ = make_shared<TrackerNode>();
    while(rclcpp::ok())
        (*tnode_).run();
    rclcpp::shutdown();
}