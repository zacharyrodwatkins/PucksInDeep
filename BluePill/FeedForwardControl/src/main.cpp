#include <Arduino.h>
#include <SPI.h>
#include "RoboClaw.h"
#include "controller.h"
#include <pi_coms.h>
#include "model.h"
#define MOTOR_LEFT 0x81
#define MOTOR_RIGHT 0x80
#define MAX(x, y) (((x) > (y)) ? (x) : (y))
#define MIN(x, y) (((x) < (y)) ? (x) : (y))

bool x_ok = true;
bool y_ok = true;
int read_count = 0;
int ser_counter = 0;

float motor_v = 24;
int start_time = 0;

MalletController controller;
GantryModel mod;

HardwareSerial Serial2(PA3, PA2);

RoboClaw roboclaw(&Serial2, 460800);
RoboClaw* roboclaw_p = &roboclaw;


void zero();

uint8_t send[SEND_SIZE];
int prev_write_time = 0;
// float finalXY[] = {0,0};
// float finalVel[] = {0,0};
float SerialReads[10] = {0};
float send_to_pi[7];
int total_effort[2] = {0};
uint8_t x_rec[20];
uint8_t y_rec[20];
uint8_t x_pid_rec[16];
uint8_t y_pid_rec[16];
const size_t NUM_VALS = 7;
const size_t NUM_BYTES_REC=NUM_VALS*__SIZEOF_FLOAT__;

// start byte (all ones) -> 1
// x (two bytes (mm)), y (two bytes (mm)) -> 4
// vx (two bytes mm/s) vy (two bytes (mm/s)) -> 4
// ax (two bytes mm/s^2) ay (two bytes mm/s^2) ->4
// t (two bytes 100ns) -> 2
// total of 15 bytes, but don't store the first so array of 14

uint8_t serial_reading_buffer[NUM_BYTES_REC];
int n_read_in_buffer = 0;

float finalXY[2] = {0,0};
float finalVel[2] = {0,0};
float finalAcc[2] = {0,0};
float path_time = 0;

void setup(){
    Serial.begin(460800);
    Serial2.begin(460800);

    controller = MalletController();
    mod = GantryModel();

    zero();

    controller.start_angles[0] =  0.0;
    controller.start_angles[1] =  0.0;
    controller.readAngle(controller.start_angles);
    delay(100); 

}

void write_to_motor(uint8_t address, int val){
  if (val<0){
    val = MAX(val,-127);
    roboclaw.BackwardM1(address, (uint8_t) abs(val));
  }
  else {
    val = MIN(val,127);
    roboclaw.ForwardM1(address ,(uint8_t) val);
  }
}

void zero() {
  float angles[2];
  float lastAngle;

  controller.readAngle(angles);
  write_to_motor(MOTOR_LEFT, -20);
  
  do {
    delay(100);
    lastAngle = angles[0];
    controller.readAngle(angles);
  } while (lastAngle != angles[0]);

  write_to_motor(MOTOR_LEFT, 0);
  delay(500);
  controller.clear_history();

  // Must reset start angles to zero, readAngle depends on their values
  controller.start_angles[0] =  0.0;
  controller.start_angles[1] =  0.0;
  controller.readAngle(controller.start_angles);
  start_time = micros();
}





// void read_serial(){
//   bool read_start = false;
//   if (n_read_in_buffer == 0){
//     // look for start byte
//     uint8_t start_buffer[1];
//     while(Serial.available()>0){
//       Serial.readBytes(start_buffer, 1);
//       if (start_buffer[0] == 0xFF){
//         read_start = true;
//         break;
//       }
//     }
//     if (read_start == false){
//       return;
//     }
//   }

//   int num_available = Serial.available();
//   int num_to_read = min( (int) NUM_BYTES_REC-n_read_in_buffer, num_available);
//   size_t num_read = Serial.readBytes((serial_reading_buffer+n_read_in_buffer),num_to_read);
//   n_read_in_buffer += num_read;



// }

int read_serial(byte path_msg[], int n_read){
  uint8_t incoming_4bytes[4];
  int read_val;
  while(Serial.available()>=4){
    Serial.readBytes(incoming_4bytes, 4);
    read_val = buffer_to_int(incoming_4bytes);
    if (read_val == 0xffffffff){
      n_read = 0;
    }


    else if (n_read == NUM_BYTES_REC){
      n_read = -1;
    }

    else if (n_read >= 0){
      for (int i=0 ; i<4; i++)
        path_msg[n_read+i] = incoming_4bytes[i];
      n_read += 4;
    }
  }
  return n_read;

}


void loop(){

  n_read_in_buffer = read_serial(serial_reading_buffer, n_read_in_buffer);

  ser_counter = Serial.available();
  if (n_read_in_buffer == NUM_BYTES_REC) {
    float vals [NUM_VALS];
    //read_count++;
    //uint8_t serial_reading_buffer[14] = {1 ,2, 3 ,4, 5, 6 , 7 , 8, 9, 10, 11, 12, 13,14};
    read_floats_from_pi(serial_reading_buffer, vals, NUM_VALS);
    // float finalXY[2] = {vals[0],vals[1]};
    // float finalVel[2] = {vals[2],vals[3]};
    // float finalAcc[2] = {vals[4],vals[5]};
    // float path_time = vals[6];

    finalXY[0] = vals[0];
    finalXY[1] = vals[1];
    finalVel[0] = vals[2];
    finalVel[1] = vals[3];
    finalAcc[0] = vals[4];
    finalAcc[1] = vals[5];
    path_time = vals[6];

    n_read_in_buffer = -1;

    start_time = micros();
    // path_time should be in seconds, start_time should be in seconds
    controller.setPath(finalXY, finalVel, finalAcc, path_time,  (1.0*start_time)/1e6);
    mod.set_coeffs(controller.x_coeffs, controller.y_coeffs);
    
  }

  float* effort;      
  float time_s =  (1.0*micros() - start_time)/1e6;
    

  if (controller.update()){
    total_effort[0] = 0;
    total_effort[1] = 0;
    write_to_motor(MOTOR_LEFT, 0);
    write_to_motor(MOTOR_RIGHT, 0);
  }

  else {
    effort = mod.get_effort(time_s);
    effort[0] = (effort[0]/motor_v)*128;
    effort[1] = (effort[1]/motor_v)*128;
    total_effort[0] = effort[0] + controller.effort_m1;
    total_effort[1] = effort[1] + controller.effort_m2;
    write_to_motor(MOTOR_LEFT, total_effort[0]);
    write_to_motor(MOTOR_RIGHT, total_effort[1]);
  }

  
  if ((millis() - prev_write_time) > 100) {
    if (Serial.availableForWrite()){
      prev_write_time = millis();
      send_to_pi[0] = (float) controller.xy[0];  // x position
      send_to_pi[1] = (float) controller.xy[1];  // y position
      send_to_pi[2] = (float) controller.current_velocity[0];  // x velocity
      send_to_pi[3] = (float) controller.current_velocity[1];  // y velocity
      send_to_pi[4] = (float) total_effort[0]; // motor1 effort
      send_to_pi[5] = (float) total_effort[1]; // motor2 effort
      send_to_pi[6] = (float) time_s; //time in milliseconds

      uint8_t msg[SEND_SIZE];
      memcpy(&msg, &send_to_pi, SEND_SIZE);
      for (int i = 0; i < 4; i++)
        Serial.write(0xff);
        
      write_to_pi(msg);
      
    }

  } 

  
}