// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from hockey_msgs:msg/PuckStatus.idl
// generated code does not contain a copyright notice

#ifndef HOCKEY_MSGS__MSG__DETAIL__PUCK_STATUS__STRUCT_H_
#define HOCKEY_MSGS__MSG__DETAIL__PUCK_STATUS__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Struct defined in msg/PuckStatus in the package hockey_msgs.
typedef struct hockey_msgs__msg__PuckStatus
{
  double x;
  double y;
  double x_vel;
  double y_vel;
} hockey_msgs__msg__PuckStatus;

// Struct for a sequence of hockey_msgs__msg__PuckStatus.
typedef struct hockey_msgs__msg__PuckStatus__Sequence
{
  hockey_msgs__msg__PuckStatus * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} hockey_msgs__msg__PuckStatus__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // HOCKEY_MSGS__MSG__DETAIL__PUCK_STATUS__STRUCT_H_
