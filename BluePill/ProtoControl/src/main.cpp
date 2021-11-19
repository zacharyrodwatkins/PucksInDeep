#include <Arduino.h>
#include <SPI.h>
#include "RoboClaw.h"
#include "controller.h"
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
float finalXY[] = {40,0};
float finalVel[] = {0,0};
float finalAcc[] = {0,0};
float SerialReads[10] = {0};
float send_to_pi[5];

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

void write_to_pi(uint8_t *buffer) {
  for (int i = 0; i<SEND_SIZE; i++) {
    Serial.write(buffer[i]);
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

void setup(){
  controller = MalletController();

  Serial.begin(9600);  // Serial communicates with RPi, if you change this baud, change on Pi too
  Serial2.begin(460800);
  delay(100);
  Serial.println("serial begun");

  zero();  // Zeros mallet to bottom left corner

  controller.setPath(finalXY,finalVel,finalAcc,1,0);
  delay(100);
  for (int i =0 ; i<6 ; i++){
    Serial.print(controller.x_coeffs[i]);
    Serial.print(" ");
    Serial.print(controller.y_coeffs[i]);
    Serial.println();
  } 
}

// void output32BitUInt(uint32_t value )
// {
//     Serial.write((value >> 24) & 0xFF );
//     Serial.write((value >> 16) & 0xFF );
//     Serial.write((value >>  8) & 0xFF );
//     Serial.write((value      ) & 0xFF );
// }

int i = 0;
void loop(){
controller.update();
  if (Serial.available() == 40) {
    for (int i = 0; i < 10 ; i ++){
      SerialReads[i] = Serial.parseFloat();
      Serial.println(SerialReads[i]);
    }
  }

  if (controller.update()) {
    write_to_motor(MOTOR_LEFT, 0);
    write_to_motor(MOTOR_RIGHT, 0);
    // delay(100);
    Serial.println("Done");
    while (true) {}
  }

  else {
  write_to_motor(MOTOR_LEFT, controller.effort_m1);
  write_to_motor(MOTOR_RIGHT, controller.effort_m2);
  }

  if ((millis() - prev_write_time) > 500) {
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