// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from hockey_msgs:msg/MalletPos.idl
// generated code does not contain a copyright notice

#ifndef HOCKEY_MSGS__MSG__DETAIL__MALLET_POS__BUILDER_HPP_
#define HOCKEY_MSGS__MSG__DETAIL__MALLET_POS__BUILDER_HPP_

#include "hockey_msgs/msg/detail/mallet_pos__struct.hpp"
#include <rosidl_runtime_cpp/message_initialization.hpp>
#include <algorithm>
#include <utility>


namespace hockey_msgs
{

namespace msg
{

namespace builder
{

class Init_MalletPos_time_on_path
{
public:
  explicit Init_MalletPos_time_on_path(::hockey_msgs::msg::MalletPos & msg)
  : msg_(msg)
  {}
  ::hockey_msgs::msg::MalletPos time_on_path(::hockey_msgs::msg::MalletPos::_time_on_path_type arg)
  {
    msg_.time_on_path = std::move(arg);
    return std::move(msg_);
  }

private:
  ::hockey_msgs::msg::MalletPos msg_;
};

class Init_MalletPos_vy
{
public:
  explicit Init_MalletPos_vy(::hockey_msgs::msg::MalletPos & msg)
  : msg_(msg)
  {}
  Init_MalletPos_time_on_path vy(::hockey_msgs::msg::MalletPos::_vy_type arg)
  {
    msg_.vy = std::move(arg);
    return Init_MalletPos_time_on_path(msg_);
  }

private:
  ::hockey_msgs::msg::MalletPos msg_;
};

class Init_MalletPos_vx
{
public:
  explicit Init_MalletPos_vx(::hockey_msgs::msg::MalletPos & msg)
  : msg_(msg)
  {}
  Init_MalletPos_vy vx(::hockey_msgs::msg::MalletPos::_vx_type arg)
  {
    msg_.vx = std::move(arg);
    return Init_MalletPos_vy(msg_);
  }

private:
  ::hockey_msgs::msg::MalletPos msg_;
};

class Init_MalletPos_y
{
public:
  explicit Init_MalletPos_y(::hockey_msgs::msg::MalletPos & msg)
  : msg_(msg)
  {}
  Init_MalletPos_vx y(::hockey_msgs::msg::MalletPos::_y_type arg)
  {
    msg_.y = std::move(arg);
    return Init_MalletPos_vx(msg_);
  }

private:
  ::hockey_msgs::msg::MalletPos msg_;
};

class Init_MalletPos_x
{
public:
  Init_MalletPos_x()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_MalletPos_y x(::hockey_msgs::msg::MalletPos::_x_type arg)
  {
    msg_.x = std::move(arg);
    return Init_MalletPos_y(msg_);
  }

private:
  ::hockey_msgs::msg::MalletPos msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::hockey_msgs::msg::MalletPos>()
{
  return hockey_msgs::msg::builder::Init_MalletPos_x();
}

}  // namespace hockey_msgs

#endif  // HOCKEY_MSGS__MSG__DETAIL__MALLET_POS__BUILDER_HPP_
