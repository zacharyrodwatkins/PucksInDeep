// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from hockey_msgs:msg/PuckStatus.idl
// generated code does not contain a copyright notice

#ifndef HOCKEY_MSGS__MSG__DETAIL__PUCK_STATUS__BUILDER_HPP_
#define HOCKEY_MSGS__MSG__DETAIL__PUCK_STATUS__BUILDER_HPP_

#include "hockey_msgs/msg/detail/puck_status__struct.hpp"
#include <rosidl_runtime_cpp/message_initialization.hpp>
#include <algorithm>
#include <utility>


namespace hockey_msgs
{

namespace msg
{

namespace builder
{

class Init_PuckStatus_y_vel
{
public:
  explicit Init_PuckStatus_y_vel(::hockey_msgs::msg::PuckStatus & msg)
  : msg_(msg)
  {}
  ::hockey_msgs::msg::PuckStatus y_vel(::hockey_msgs::msg::PuckStatus::_y_vel_type arg)
  {
    msg_.y_vel = std::move(arg);
    return std::move(msg_);
  }

private:
  ::hockey_msgs::msg::PuckStatus msg_;
};

class Init_PuckStatus_x_vel
{
public:
  explicit Init_PuckStatus_x_vel(::hockey_msgs::msg::PuckStatus & msg)
  : msg_(msg)
  {}
  Init_PuckStatus_y_vel x_vel(::hockey_msgs::msg::PuckStatus::_x_vel_type arg)
  {
    msg_.x_vel = std::move(arg);
    return Init_PuckStatus_y_vel(msg_);
  }

private:
  ::hockey_msgs::msg::PuckStatus msg_;
};

class Init_PuckStatus_y
{
public:
  explicit Init_PuckStatus_y(::hockey_msgs::msg::PuckStatus & msg)
  : msg_(msg)
  {}
  Init_PuckStatus_x_vel y(::hockey_msgs::msg::PuckStatus::_y_type arg)
  {
    msg_.y = std::move(arg);
    return Init_PuckStatus_x_vel(msg_);
  }

private:
  ::hockey_msgs::msg::PuckStatus msg_;
};

class Init_PuckStatus_x
{
public:
  Init_PuckStatus_x()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_PuckStatus_y x(::hockey_msgs::msg::PuckStatus::_x_type arg)
  {
    msg_.x = std::move(arg);
    return Init_PuckStatus_y(msg_);
  }

private:
  ::hockey_msgs::msg::PuckStatus msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::hockey_msgs::msg::PuckStatus>()
{
  return hockey_msgs::msg::builder::Init_PuckStatus_x();
}

}  // namespace hockey_msgs

#endif  // HOCKEY_MSGS__MSG__DETAIL__PUCK_STATUS__BUILDER_HPP_
