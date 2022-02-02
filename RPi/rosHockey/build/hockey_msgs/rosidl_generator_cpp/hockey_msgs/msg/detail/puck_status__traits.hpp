// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from hockey_msgs:msg/PuckStatus.idl
// generated code does not contain a copyright notice

#ifndef HOCKEY_MSGS__MSG__DETAIL__PUCK_STATUS__TRAITS_HPP_
#define HOCKEY_MSGS__MSG__DETAIL__PUCK_STATUS__TRAITS_HPP_

#include "hockey_msgs/msg/detail/puck_status__struct.hpp"
#include <rosidl_runtime_cpp/traits.hpp>
#include <stdint.h>
#include <type_traits>

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<hockey_msgs::msg::PuckStatus>()
{
  return "hockey_msgs::msg::PuckStatus";
}

template<>
inline const char * name<hockey_msgs::msg::PuckStatus>()
{
  return "hockey_msgs/msg/PuckStatus";
}

template<>
struct has_fixed_size<hockey_msgs::msg::PuckStatus>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<hockey_msgs::msg::PuckStatus>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<hockey_msgs::msg::PuckStatus>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // HOCKEY_MSGS__MSG__DETAIL__PUCK_STATUS__TRAITS_HPP_
