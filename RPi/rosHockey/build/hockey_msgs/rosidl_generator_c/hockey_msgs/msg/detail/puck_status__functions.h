// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from hockey_msgs:msg/PuckStatus.idl
// generated code does not contain a copyright notice

#ifndef HOCKEY_MSGS__MSG__DETAIL__PUCK_STATUS__FUNCTIONS_H_
#define HOCKEY_MSGS__MSG__DETAIL__PUCK_STATUS__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_runtime_c/visibility_control.h"
#include "hockey_msgs/msg/rosidl_generator_c__visibility_control.h"

#include "hockey_msgs/msg/detail/puck_status__struct.h"

/// Initialize msg/PuckStatus message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * hockey_msgs__msg__PuckStatus
 * )) before or use
 * hockey_msgs__msg__PuckStatus__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_hockey_msgs
bool
hockey_msgs__msg__PuckStatus__init(hockey_msgs__msg__PuckStatus * msg);

/// Finalize msg/PuckStatus message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_hockey_msgs
void
hockey_msgs__msg__PuckStatus__fini(hockey_msgs__msg__PuckStatus * msg);

/// Create msg/PuckStatus message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * hockey_msgs__msg__PuckStatus__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_hockey_msgs
hockey_msgs__msg__PuckStatus *
hockey_msgs__msg__PuckStatus__create();

/// Destroy msg/PuckStatus message.
/**
 * It calls
 * hockey_msgs__msg__PuckStatus__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_hockey_msgs
void
hockey_msgs__msg__PuckStatus__destroy(hockey_msgs__msg__PuckStatus * msg);


/// Initialize array of msg/PuckStatus messages.
/**
 * It allocates the memory for the number of elements and calls
 * hockey_msgs__msg__PuckStatus__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_hockey_msgs
bool
hockey_msgs__msg__PuckStatus__Sequence__init(hockey_msgs__msg__PuckStatus__Sequence * array, size_t size);

/// Finalize array of msg/PuckStatus messages.
/**
 * It calls
 * hockey_msgs__msg__PuckStatus__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_hockey_msgs
void
hockey_msgs__msg__PuckStatus__Sequence__fini(hockey_msgs__msg__PuckStatus__Sequence * array);

/// Create array of msg/PuckStatus messages.
/**
 * It allocates the memory for the array and calls
 * hockey_msgs__msg__PuckStatus__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_hockey_msgs
hockey_msgs__msg__PuckStatus__Sequence *
hockey_msgs__msg__PuckStatus__Sequence__create(size_t size);

/// Destroy array of msg/PuckStatus messages.
/**
 * It calls
 * hockey_msgs__msg__PuckStatus__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_hockey_msgs
void
hockey_msgs__msg__PuckStatus__Sequence__destroy(hockey_msgs__msg__PuckStatus__Sequence * array);

#ifdef __cplusplus
}
#endif

#endif  // HOCKEY_MSGS__MSG__DETAIL__PUCK_STATUS__FUNCTIONS_H_
