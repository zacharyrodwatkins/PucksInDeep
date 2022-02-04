// generated from rosidl_typesupport_fastrtps_cpp/resource/idl__type_support.cpp.em
// with input from hockey_msgs:msg/PuckStatus.idl
// generated code does not contain a copyright notice
#include "hockey_msgs/msg/detail/puck_status__rosidl_typesupport_fastrtps_cpp.hpp"
#include "hockey_msgs/msg/detail/puck_status__struct.hpp"

#include <limits>
#include <stdexcept>
#include <string>
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_fastrtps_cpp/identifier.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_fastrtps_cpp/wstring_conversion.hpp"
#include "fastcdr/Cdr.h"


// forward declaration of message dependencies and their conversion functions

namespace hockey_msgs
{

namespace msg
{

namespace typesupport_fastrtps_cpp
{

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_hockey_msgs
cdr_serialize(
  const hockey_msgs::msg::PuckStatus & ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  // Member: x
  cdr << ros_message.x;
  // Member: y
  cdr << ros_message.y;
  // Member: x_vel
  cdr << ros_message.x_vel;
  // Member: y_vel
  cdr << ros_message.y_vel;
  return true;
}

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_hockey_msgs
cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  hockey_msgs::msg::PuckStatus & ros_message)
{
  // Member: x
  cdr >> ros_message.x;

  // Member: y
  cdr >> ros_message.y;

  // Member: x_vel
  cdr >> ros_message.x_vel;

  // Member: y_vel
  cdr >> ros_message.y_vel;

  return true;
}

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_hockey_msgs
get_serialized_size(
  const hockey_msgs::msg::PuckStatus & ros_message,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // Member: x
  {
    size_t item_size = sizeof(ros_message.x);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: y
  {
    size_t item_size = sizeof(ros_message.y);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: x_vel
  {
    size_t item_size = sizeof(ros_message.x_vel);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: y_vel
  {
    size_t item_size = sizeof(ros_message.y_vel);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  return current_alignment - initial_alignment;
}

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_hockey_msgs
max_serialized_size_PuckStatus(
  bool & full_bounded,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;
  (void)full_bounded;


  // Member: x
  {
    size_t array_size = 1;

    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }

  // Member: y
  {
    size_t array_size = 1;

    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }

  // Member: x_vel
  {
    size_t array_size = 1;

    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }

  // Member: y_vel
  {
    size_t array_size = 1;

    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }

  return current_alignment - initial_alignment;
}

static bool _PuckStatus__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  auto typed_message =
    static_cast<const hockey_msgs::msg::PuckStatus *>(
    untyped_ros_message);
  return cdr_serialize(*typed_message, cdr);
}

static bool _PuckStatus__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  auto typed_message =
    static_cast<hockey_msgs::msg::PuckStatus *>(
    untyped_ros_message);
  return cdr_deserialize(cdr, *typed_message);
}

static uint32_t _PuckStatus__get_serialized_size(
  const void * untyped_ros_message)
{
  auto typed_message =
    static_cast<const hockey_msgs::msg::PuckStatus *>(
    untyped_ros_message);
  return static_cast<uint32_t>(get_serialized_size(*typed_message, 0));
}

static size_t _PuckStatus__max_serialized_size(bool & full_bounded)
{
  return max_serialized_size_PuckStatus(full_bounded, 0);
}

static message_type_support_callbacks_t _PuckStatus__callbacks = {
  "hockey_msgs::msg",
  "PuckStatus",
  _PuckStatus__cdr_serialize,
  _PuckStatus__cdr_deserialize,
  _PuckStatus__get_serialized_size,
  _PuckStatus__max_serialized_size
};

static rosidl_message_type_support_t _PuckStatus__handle = {
  rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
  &_PuckStatus__callbacks,
  get_message_typesupport_handle_function,
};

}  // namespace typesupport_fastrtps_cpp

}  // namespace msg

}  // namespace hockey_msgs

namespace rosidl_typesupport_fastrtps_cpp
{

template<>
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_EXPORT_hockey_msgs
const rosidl_message_type_support_t *
get_message_type_support_handle<hockey_msgs::msg::PuckStatus>()
{
  return &hockey_msgs::msg::typesupport_fastrtps_cpp::_PuckStatus__handle;
}

}  // namespace rosidl_typesupport_fastrtps_cpp

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, hockey_msgs, msg, PuckStatus)() {
  return &hockey_msgs::msg::typesupport_fastrtps_cpp::_PuckStatus__handle;
}

#ifdef __cplusplus
}
#endif
