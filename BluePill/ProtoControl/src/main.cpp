#include <Arduino.h>
#include <SPI.h>
#include "RoboClaw.h"
#include "controller.h"
#include <pi_coms.h>
#define MOTOR_LEFT 0x81
#define MOTOR_RIGHT 0x80
#define MAX(x, y) (((x) > (y)) ? (x) : (y))
#define MIN(x, y) (((x) < (y)) ? (x) : (y))
#define SEND_SIZE 20

MalletController controller;
HardwareSerial Serial2(PA3, PA2);

RoboClaw roboclaw(&Serial2, 460800);
RoboClaw* roboclaw_p = &roboclaw;

float temp_float = 0;
uint8_t send[SEND_SIZE];

int prev_write_time = 0;
float finalXY[] = {0,0};
float finalVel[] = {0,0};
float finalAcc[] = {0,0};
float SerialReads[10] = {0};
float send_to_pi[5];
uint8_t x_rec[20];
uint8_t y_rec[20];

void zero();

void setup(){


  controller = MalletController();

  Serial.begin(1000000);//1000000 for pi Serial communicates with RPi, if you change this baud, change on Pi too
  Serial2.begin(460800);

  zero();
  controller.setPath(finalXY,finalVel,finalAcc,0.5,0);
  delay(100);  
}

void write_to_motor(uint8_t address, int val){
  if (val<0){
    roboclaw.ForwardM1(address ,(uint8_t) val);
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
}


void loop(){

  if (Serial.available() >= 40) {
    float x_coefs[4]; // these are final x,v,a,t
    float y_coefs[4];
    if (read_from_pi(x_rec, x_coefs) && read_from_pi(y_rec, y_coefs)) {
      // checksum valid on x data received from pi
      float finalXY[2] = {x_coefs[0],y_coefs[0]};
      float finalVel[2]   = {x_coefs[1], y_coefs[1]};
      float finalAcc[2] = {x_coefs[2], y_coefs[2]};
      float path_time = x_coefs[3];


      controller.setPath(finalXY, finalVel, finalAcc, path_time,  micros() - controller.start_time);
    }
  }

  if (controller.update()){
    write_to_motor(MOTOR_LEFT, 0);
    write_to_motor(MOTOR_RIGHT, 0);
  }

  else {
    write_to_motor(MOTOR_LEFT, controller.effort_m1);
    write_to_motor(MOTOR_RIGHT, controller.effort_m2);
  }

  if ((millis() - prev_write_time) > 100) {
    prev_write_time = millis();
    send_to_pi[0] = controller.xy[0];  // x position
    send_to_pi[1] =  controller.xy[1];  // y position
    send_to_pi[2] = controller.current_velocity[0];  // x velocity
    send_to_pi[3] =  controller.current_velocity[1];  // y velocity
    send_to_pi[4] = send_to_pi[0] + send_to_pi[1] + send_to_pi[2] + send_to_pi[3];  // checksum

    uint8_t msg[20];
    memcpy(&msg, &send_to_pi, 20);
    write_to_pi(msg);
  } 

  delayMicroseconds(150);
}

