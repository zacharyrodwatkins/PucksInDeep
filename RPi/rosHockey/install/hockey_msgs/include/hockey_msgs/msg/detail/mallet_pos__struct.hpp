// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from hockey_msgs:msg/MalletPos.idl
// generated code does not contain a copyright notice

#ifndef HOCKEY_MSGS__MSG__DETAIL__MALLET_POS__STRUCT_HPP_
#define HOCKEY_MSGS__MSG__DETAIL__MALLET_POS__STRUCT_HPP_

#include <rosidl_runtime_cpp/bounded_vector.hpp>
#include <rosidl_runtime_cpp/message_initialization.hpp>
#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>


#ifndef _WIN32
# define DEPRECATED__hockey_msgs__msg__MalletPos __attribute__((deprecated))
#else
# define DEPRECATED__hockey_msgs__msg__MalletPos __declspec(deprecated)
#endif

namespace hockey_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct MalletPos_
{
  using Type = MalletPos_<ContainerAllocator>;

  explicit MalletPos_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->x = 0.0;
      this->y = 0.0;
      this->vx = 0.0;
      this->vy = 0.0;
      this->time_on_path = 0.0;
    }
  }

  explicit MalletPos_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->x = 0.0;
      this->y = 0.0;
      this->vx = 0.0;
      this->vy = 0.0;
      this->time_on_path = 0.0;
    }
  }

  // field types and members
  using _x_type =
    double;
  _x_type x;
  using _y_type =
    double;
  _y_type y;
  using _vx_type =
    double;
  _vx_type vx;
  using _vy_type =
    double;
  _vy_type vy;
  using _time_on_path_type =
    double;
  _time_on_path_type time_on_path;

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
  Type & set__vx(
    const double & _arg)
  {
    this->vx = _arg;
    return *this;
  }
  Type & set__vy(
    const double & _arg)
  {
    this->vy = _arg;
    return *this;
  }
  Type & set__time_on_path(
    const double & _arg)
  {
    this->time_on_path = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    hockey_msgs::msg::MalletPos_<ContainerAllocator> *;
  using ConstRawPtr =
    const hockey_msgs::msg::MalletPos_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<hockey_msgs::msg::MalletPos_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<hockey_msgs::msg::MalletPos_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      hockey_msgs::msg::MalletPos_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<hockey_msgs::msg::MalletPos_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      hockey_msgs::msg::MalletPos_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<hockey_msgs::msg::MalletPos_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<hockey_msgs::msg::MalletPos_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<hockey_msgs::msg::MalletPos_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__hockey_msgs__msg__MalletPos
    std::shared_ptr<hockey_msgs::msg::MalletPos_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__hockey_msgs__msg__MalletPos
    std::shared_ptr<hockey_msgs::msg::MalletPos_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const MalletPos_ & other) const
  {
    if (this->x != other.x) {
      return false;
    }
    if (this->y != other.y) {
      return false;
    }
    if (this->vx != other.vx) {
      return false;
    }
    if (this->vy != other.vy) {
      return false;
    }
    if (this->time_on_path != other.time_on_path) {
      return false;
    }
    return true;
  }
  bool operator!=(const MalletPos_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct MalletPos_

// alias to use template instance with default allocator
using MalletPos =
  hockey_msgs::msg::MalletPos_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace hockey_msgs

#endif  // HOCKEY_MSGS__MSG__DETAIL__MALLET_POS__STRUCT_HPP_
