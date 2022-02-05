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


int motor_v = 23.6;

MalletController controller;
GantryModel mod;

HardwareSerial Serial2(PA3, PA2);

RoboClaw roboclaw(&Serial2, 460800);
RoboClaw* roboclaw_p = &roboclaw;

int start_time;
float path_time;


void zero();

uint8_t send[SEND_SIZE];
int prev_write_time = 0;
float finalXY[] = {0,0};
float finalVel[] = {0,0};
float finalAcc[] = {0,0};
float SerialReads[10] = {0};
float send_to_pi[7];
int total_effort[2] = {0};
uint8_t x_rec[20];
uint8_t y_rec[20];
uint8_t x_pid_rec[16];
uint8_t y_pid_rec[16];

void setup(){
    Serial.begin(1000000);
    Serial2.begin(460800);

    controller = MalletController();
    mod = GantryModel();

    zero();

    controller.start_angles[0] =  0.0;
    controller.start_angles[1] =  0.0;
    controller.readAngle(controller.start_angles);
    delay(100); 


    
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
 

  if (Serial.available() == 40) {
    float x_coefs[4]; // these are final x,v,a,t
    float y_coefs[4];
    if (read_from_pi(x_rec, x_coefs) && read_from_pi(y_rec, y_coefs)) {
      // checksum valid on x data received from pi
      float finalXY[2] = {x_coefs[0],y_coefs[0]};
      float finalVel[2]   = {x_coefs[1], y_coefs[1]};
      float finalAcc[2] = {x_coefs[2], y_coefs[2]};
      float path_time = x_coefs[3]/1000.0;

      start_time = micros();
      controller.setPath(finalXY, finalVel, finalAcc, path_time,  (1.0*start_time)/1e6);
      mod.set_coeffs(controller.x_coeffs, controller.y_coeffs);
    }
  }

    float* effort;      
    float time_s =  (1.0*micros() - start_time)/1e6;
    effort = mod.get_effort(time_s);
    effort[0] = (effort[0]/motor_v)*128;
    effort[1] = (effort[1]/motor_v)*128;



  if (controller.update()){
    total_effort[0] = 0;
    total_effort[1] = 0;
    write_to_motor(MOTOR_LEFT, 0);
    write_to_motor(MOTOR_RIGHT, 0);
  }

  else {
    total_effort[0] = controller.effort_m1+effort[0];
    total_effort[1] = controller.effort_m2+effort[1];
    write_to_motor(MOTOR_LEFT, total_effort[0]);
    write_to_motor(MOTOR_RIGHT, total_effort[1]);
  }

  
if ((millis() - prev_write_time) > 500) {
    prev_write_time = millis();
    send_to_pi[0] = controller.xy[0];  // x position
    send_to_pi[1] = controller.xy[1];  // y position
    send_to_pi[2] = controller.current_velocity[0];  // x velocity
    send_to_pi[3] = controller.current_velocity[1];  // y velocity
    send_to_pi[4] = (float) total_effort[0]; // motor1 effort
    send_to_pi[5] = (float) total_effort[1]; // motor2 effort
    send_to_pi[6] = (float) time_s*1e3; //time in seconds
    

    uint8_t msg[SEND_SIZE];
    memcpy(&msg, &send_to_pi, SEND_SIZE);
    write_to_pi(msg);
  } 

  
}