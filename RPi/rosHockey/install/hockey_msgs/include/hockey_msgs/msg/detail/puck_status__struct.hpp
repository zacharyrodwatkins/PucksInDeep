// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from hockey_msgs:msg/PuckStatus.idl
// generated code does not contain a copyright notice

#ifndef HOCKEY_MSGS__MSG__DETAIL__PUCK_STATUS__STRUCT_HPP_
#define HOCKEY_MSGS__MSG__DETAIL__PUCK_STATUS__STRUCT_HPP_

#include <rosidl_runtime_cpp/bounded_vector.hpp>
#include <rosidl_runtime_cpp/message_initialization.hpp>
#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>


#ifndef _WIN32
# define DEPRECATED__hockey_msgs__msg__PuckStatus __attribute__((deprecated))
#else
# define DEPRECATED__hockey_msgs__msg__PuckStatus __declspec(deprecated)
#endif

namespace hockey_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct PuckStatus_
{
  using Type = PuckStatus_<ContainerAllocator>;

  explicit PuckStatus_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->x = 0.0;
      this->y = 0.0;
      this->x_vel = 0.0;
      this->y_vel = 0.0;
    }
  }

  explicit PuckStatus_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->x = 0.0;
      this->y = 0.0;
      this->x_vel = 0.0;
      this->y_vel = 0.0;
    }
  }

  // field types and members
  using _x_type =
    double;
  _x_type x;
  using _y_type =
    double;
  _y_type y;
  using _x_vel_type =
    double;
  _x_vel_type x_vel;
  using _y_vel_type =
    double;
  _y_vel_type y_vel;

  // setters for named parameter idiom
  Type & set__x(
    const double & _arg)
  {
    this->x = _arg;
    return *this;
  }
  Type & set__y(
    const double & _arg)
  {
    this->y = _arg;
    return *this;
  }
  Type & set__x_vel(
    const double & _arg)
  {
    this->x_vel = _arg;
    return *this;
  }
  Type & set__y_vel(
    const double & _arg)
  {
    this->y_vel = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    hockey_msgs::msg::PuckStatus_<ContainerAllocator> *;
  using ConstRawPtr =
    const hockey_msgs::msg::PuckStatus_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<hockey_msgs::msg::PuckStatus_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<hockey_msgs::msg::PuckStatus_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      hockey_msgs::msg::PuckStatus_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<hockey_msgs::msg::PuckStatus_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      hockey_msgs::msg::PuckStatus_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<hockey_msgs::msg::PuckStatus_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<hockey_msgs::msg::PuckStatus_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<hockey_msgs::msg::PuckStatus_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__hockey_msgs__msg__PuckStatus
    std::shared_ptr<hockey_msgs::msg::PuckStatus_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__hockey_msgs__msg__PuckStatus
    std::shared_ptr<hockey_msgs::msg::PuckStatus_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const PuckStatus_ & other) const
  {
    if (this->x != other.x) {
      return false;
    }
    if (this->y != other.y) {
      return false;
    }
    if (this->x_vel != other.x_vel) {
      return false;
    }
    if (this->y_vel != other.y_vel) {
      return false;
    }
    return true;
  }
  bool operator!=(const PuckStatus_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct PuckStatus_

// alias to use template instance with default allocator
using PuckStatus =
  hockey_msgs::msg::PuckStatus_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace hockey_msgs

#endif  // HOCKEY_MSGS__MSG__DETAIL__PUCK_STATUS__STRUCT_HPP_
