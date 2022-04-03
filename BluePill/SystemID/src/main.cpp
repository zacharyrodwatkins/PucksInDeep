#include <Arduino.h>
#include <SPI.h>
#include "RoboClaw.h"
#include "controller.h"
#include <pi_coms.h>
#include "path.h"
#include "model.h"
#include <cmath>
#define MOTOR_LEFT 0x81
#define MOTOR_RIGHT 0x80
#define MAX(x, y) (((x) > (y)) ? (x) : (y))
#define MIN(x, y) (((x) < (y)) ? (x) : (y))

bool x_ok = true;
bool y_ok = true;
int read_count = 0;
int ser_counter = 0;

const float SUPPLY_V = 24;
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

FUNCTION func_type;
DIRECTION dir;
float char_time;
float max_v;
tester t;
float v[2] = {0,0};

int ramp_count = 0;


FUNCTION get_func_type(float read_val){

  int val = round(read_val);
  FUNCTION func_type;
  switch (val)
  {
  case 1:
    func_type = STEP;
    break;
  case 2:
    func_type = DOUBLE_STEP;
    break;
  case 3:
    func_type = RAMP;
    break;
  case 4:
    func_type = TRIANGLE;
    break;
  case 5:
    func_type = RAMP_AND_STAY;
    break;

  default:
    func_type = NONE;
  }
  return func_type;
}

DIRECTION get_dir(float read_val){
  int val = round(read_val);
  if (val==0)
    return Y;
  else
    return X;
}

void setup(){
    Serial.begin(460800);
    Serial2.begin(460800);

    t = tester();
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

void move_to_middle_x(){
  controller.update();
  while(controller.xy[0]<25){
    write_to_motor(MOTOR_LEFT, 20);
    write_to_motor(MOTOR_RIGHT, 20);
    controller.update();
    delayMicroseconds(150);
  }
  write_to_motor(MOTOR_LEFT, 0);
  write_to_motor(MOTOR_RIGHT, 0);
}

void move_to_middle_y(){
  controller.update();
  while(controller.xy[1]<25){
    write_to_motor(MOTOR_LEFT, 20);
    write_to_motor(MOTOR_RIGHT, -20);
    controller.update();
    delayMicroseconds(150);
  }
  write_to_motor(MOTOR_LEFT, 0);
  write_to_motor(MOTOR_RIGHT, 0);
}

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
    read_floats_from_pi(serial_reading_buffer, vals, NUM_VALS);
    func_type = get_func_type(round(vals[0]));
    dir = get_dir(round(vals[1]));
    char_time = vals[2];
    max_v = vals[3];
    n_read_in_buffer = -1;
    t.set_function(func_type, dir, char_time, max_v);


    ramp_count = 0;


    zero();
    if (dir==Y)
      move_to_middle_x();
    else 
      move_to_middle_y();

    delay(500);    
    start_time = micros();
    // path_time should be in seconds, start_time should be in seconds
  }

  float time_s =  (1.0*micros() - start_time)/1e6;

  controller.update();

  t.get_efforts(time_s, v);
  total_effort[0] = v[0]*128.0/SUPPLY_V;
  total_effort[1] = v[1]*128.0/SUPPLY_V;
  
  write_to_motor(MOTOR_LEFT, total_effort[0]);
  write_to_motor(MOTOR_RIGHT, total_effort[1]);
  // write_to_motor(MOTOR_LEFT, total_effort[0]);


  
  if ((millis() - prev_write_time) > 1) {
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

  delayMicroseconds(150);
  
}