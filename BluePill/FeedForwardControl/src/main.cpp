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
#define SEND_SIZE 20



MalletController controller;
GantryModel mod;

HardwareSerial Serial2(PA3, PA2);

RoboClaw roboclaw(&Serial2, 460800);
RoboClaw* roboclaw_p = &roboclaw;

int start_time;
float path_time;

void zero();

void setup(){
    Serial.begin(9600);
    Serial2.begin(460800);

    controller = MalletController();
    mod = GantryModel();

    zero();

    controller.start_angles[0] =  0.0;
    controller.start_angles[1] =  0.0;
    controller.readAngle(controller.start_angles);
    delay(100); 
    pinMode(PA12,OUTPUT);


    float finalxy[2] = {35,60};
    float finalvel[2] = {20,-20};
    float finalacc[2] = {0,0};
    path_time = 1;
    controller.setPath(finalxy, finalvel, finalacc, path_time,0);
    mod.set_coeffs(controller.x_coeffs, controller.y_coeffs);
    start_time = micros();

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
}


void loop(){

    float* effort;
    int t = micros();
    if (t-start_time<path_time*1000000){
        
        float time_s = float(t-start_time)/1000000;
        effort = mod.get_effort(time_s);
        effort[0] = (effort[0]/23.6)*128;
        effort[1] = (effort[1]/23.6)*128;
  if (controller.update()){
    write_to_motor(MOTOR_LEFT, 0);
    write_to_motor(MOTOR_RIGHT, 0);
  }

  else {
    write_to_motor(MOTOR_LEFT, controller.effort_m1+effort[0]);
    write_to_motor(MOTOR_RIGHT, controller.effort_m2+effort[1]);

    // Serial.print(controller.effort_m1);
    // Serial.print(" ");
    // Serial.print(controller.effort_m2);
    // Serial.println();
  }
}
}