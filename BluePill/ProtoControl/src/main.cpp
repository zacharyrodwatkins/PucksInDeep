#include <Arduino.h>
#include <SPI.h>
#include "RoboClaw.h"
#include "controller.h"
#define MOTOR_LEFT 0x81
#define MOTOR_RIGHT 0x80
#define MAX(x, y) (((x) > (y)) ? (x) : (y))
#define MIN(x, y) (((x) < (y)) ? (x) : (y))
#define SEND_SIZE 4

MalletController controller;
HardwareSerial Serial2(PA3, PA2);

RoboClaw roboclaw(&Serial2, 460800);
RoboClaw* roboclaw_p = &roboclaw;

float temp_float = 0;
uint8_t send[SEND_SIZE];

int prev_write_time = 0;
float finalXY[] = {0,60};
float finalVel[] = {0,60};
float finalAcc[] = {0,0};

float SerialReads[10] = {0};

void setup(){


  controller = MalletController();

  Serial.begin(9600);
  Serial2.begin(460800);

  controller.setPath(finalXY,finalVel,finalAcc,0.5,0);
  delay(100);
  // for (int i =0 ; i<6 ; i++){
  //   Serial.print(controller.x_coeffs[i]);
  //   Serial.print(" ");
  //   Serial.print(controller.y_coeffs[i]);
  //   Serial.println();
  // }
  
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

void write_to_pi(uint8_t *buffer) {
  for (int i = 0; i<4; i++) {
    Serial.write(buffer[i]);
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

  // if (controller.update()){
  //   write_to_motor(MOTOR_LEFT, 0);
  //   write_to_motor(MOTOR_RIGHT, 0);
  //   // delay(100);
  //   Serial.println("Done");
  //   while (true) {}
  //   }

  else {
  write_to_motor(MOTOR_LEFT, controller.effort_m1);
  write_to_motor(MOTOR_RIGHT, controller.effort_m2);
  }

  if ((millis() - prev_write_time) > 1000) {
    prev_write_time = millis();
    float x = 100.0;
    uint8_t x_asbyes[4];
    memcpy(&x_asbyes, &x, 4);
    write_to_pi(x_asbyes);
    // Serial.write(x_asbyes[0]);
    // Serial.write(x_asbyes[1]);
    // Serial.write(x_asbyes[2]);
    // Serial.write(x_asbyes[3]);
  } 

  delayMicroseconds(150);
}