// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from hockey_msgs:msg/PuckStatus.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "hockey_msgs/msg/detail/puck_status__rosidl_typesupport_introspection_c.h"
#include "hockey_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "hockey_msgs/msg/detail/puck_status__functions.h"
#include "hockey_msgs/msg/detail/puck_status__struct.h"


#ifdef __cplusplus
extern "C"
{
#endif

void PuckStatus__rosidl_typesupport_introspection_c__PuckStatus_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  hockey_msgs__msg__PuckStatus__init(message_memory);
}

void PuckStatus__rosidl_typesupport_introspection_c__PuckStatus_fini_function(void * message_memory)
{
  hockey_msgs__msg__PuckStatus__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember PuckStatus__rosidl_typesupport_introspection_c__PuckStatus_message_member_array[4] = {
  {
    "x",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(hockey_msgs__msg__PuckStatus, x),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "y",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(hockey_msgs__msg__PuckStatus, y),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "x_vel",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(hockey_msgs__msg__PuckStatus, x_vel),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "y_vel",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(hockey_msgs__msg__PuckStatus, y_vel),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers PuckStatus__rosidl_typesupport_introspection_c__PuckStatus_message_members = {
  "hockey_msgs__msg",  // message namespace
  "PuckStatus",  // message name
  4,  // number of fields
  sizeof(hockey_msgs__msg__PuckStatus),
  PuckStatus__rosidl_typesupport_introspection_c__PuckStatus_message_member_array,  // message members
  PuckStatus__rosidl_typesupport_introspection_c__PuckStatus_init_function,  // function to initialize message memory (memory has to be allocated)
  PuckStatus__rosidl_typesupport_introspection_c__PuckStatus_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t PuckStatus__rosidl_typesupport_introspection_c__PuckStatus_message_type_support_handle = {
  0,
  &PuckStatus__rosidl_typesupport_introspection_c__PuckStatus_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_hockey_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, hockey_msgs, msg, PuckStatus)() {
  if (!PuckStatus__rosidl_typesupport_introspection_c__PuckStatus_message_type_support_handle.typesupport_identifier) {
    PuckStatus__rosidl_typesupport_introspection_c__PuckStatus_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &PuckStatus__rosidl_typesupport_introspection_c__PuckStatus_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
