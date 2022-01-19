#include <Arduino.h>
#include <SPI.h>
#include "RoboClaw.h"
#include "controller.h"
#include <pi_coms.h>
#define MOTOR_LEFT 0x81
#define MOTOR_RIGHT 0x80
#define MAX(x, y) (((x) > (y)) ? (x) : (y))
#define MIN(x, y) (((x) < (y)) ? (x) : (y))
#define SEND_SIZE 24
#define CURRENT_READ_HIGH PB0
#define CURRENT_READ_LOW PB1

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
float send_to_pi[6];
uint8_t x_rec[20];
uint8_t y_rec[20];
float current_reading_high = 0;
float current_reading_low = 0;
float current = 0; 
float A_per_V = 1000.0/12;
int speed = 0;
void zero();


void setup(){

  pinMode(CURRENT_READ_HIGH, INPUT_ANALOG);
  pinMode(CURRENT_READ_LOW, INPUT_ANALOG);
  controller = MalletController();

  Serial.begin(1000000);//1000000 for pi Serial communicates with RPi, if you change this baud, change on Pi too
  Serial2.begin(460800);

  zero();
  delay(100);
  
  while (true)
  {
    if (Serial.available()>0){
      speed = Serial.read();
      break;
    }
  }


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

  int analogVal1 = analogRead(CURRENT_READ_HIGH);
  current_reading_high = 3.3*float(analogVal1)/(1023);
  int analogVal2 = analogRead(CURRENT_READ_LOW);
  current_reading_low = 3.3*float(analogVal2)/(1023);
  current = (current_reading_high-current_reading_low)*A_per_V;

  controller.update();


  if (controller.xy[0]<60){
    write_to_motor(MOTOR_LEFT, speed);
    write_to_motor(MOTOR_RIGHT, -1*speed);
  }

  else {
    write_to_motor(MOTOR_LEFT, speed);
    write_to_motor(MOTOR_RIGHT, -1*speed);
    while(true);
  }


  if ((millis() - prev_write_time) > 100) {
    prev_write_time = millis();
    send_to_pi[0] = float(analogVal1);//controller.xy[0];  // x position
    send_to_pi[1] =  float(analogVal2);//controller.xy[1];  // y position
    send_to_pi[2] = current_reading_high; // controller.current_velocity[0];  // x velocity
    send_to_pi[3] =  current_reading_low; //controller.current_velocity[1];  // y velocity
    send_to_pi[4] = current;
    send_to_pi[5] = 1.0*prev_write_time;
    //send_to_pi[4] = send_to_pi[0] + send_to_pi[1] + send_to_pi[2] + send_to_pi[3];  // checksum

    uint8_t msg[SEND_SIZE];
    memcpy(&msg, &send_to_pi, SEND_SIZE);
    write_to_pi(msg);
  } 

  

  delayMicroseconds(150);
}

