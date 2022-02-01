#include <Arduino.h>
#include <SPI.h>
#include "RoboClaw.h"
#include "controller.h"
#include <pi_coms.h>
#include <math.h>
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

float* voltage_from_time(int t);

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
int speed = 4;
int start_time;
int t;
bool written = false;
float volts[2];
int right_speed;
int left_speed;


void setup(){
  controller = MalletController();

  Serial.begin(1000000);//1000000 for pi Serial communicates with RPi, if you change this baud, change on Pi too
  Serial2.begin(460800);

  delay(100);
  
  start_time = millis();
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

void voltage_from_time(int t, float v[2]) {
  float seconds = 0.001*t;
  int H1 = 0;
  if (seconds > 0.1) {
    H1 = 1;
  }
  // DIAGONAL
  // float V1 = -(5040.0*H1)/1423.0 + (2520.0)/1423.0 + (2280.0*seconds)/1423.0 + (2280.0*H1*(2.0*seconds - 1.0/5.0))/1423.0;
  // float V2 =  (11600.0*H1)/1423.0 - (5800.0)/1423.0 - (80600.0*seconds)/1423.0 + (80600.0*H1*(2.0*seconds - 1.0/5.0))/1423.0;

  //FROM POLYNOMIAL
  // float V1 = (2129*pow(seconds,4))/4000 + (2053*pow(seconds,3))/5000 + (831*pow(seconds,2))/2000 + (367*seconds)/1250 + 589/5000;
  // float V2 = (4087*pow(seconds,4))/4000 - (823*pow(seconds,3))/5000 - (723*pow(seconds,2))/2000 + (151*seconds)/1250 + 529/5000;
  float V1 = (403*pow(seconds,4))/800 - (93*pow(seconds,3))/250 - (3111*pow(seconds,2))/250 + (1067*seconds)/1250 - 135781/20000;
  float V2 = (57*pow(seconds,4))/4000 - (10261*pow(seconds,3))/2500 - (31719*pow(seconds,2))/1250 - (1651*seconds)/625 + 24417/4000;

  v[0] = V1;
  v[1] = V2;
}


void loop(){
  t = millis();
  controller.update();

  if (t-start_time < 500) {
    voltage_from_time(t-start_time, volts);
    right_speed = max(-127, min(127, (int)(volts[0]*127/24)));
    left_speed = max(-127, min(127, (int)(volts[1]*127/24)));
    write_to_motor(MOTOR_RIGHT, left_speed);
    write_to_motor(MOTOR_LEFT, right_speed);

    if (millis()-prev_write_time > 10){
      prev_write_time = millis();
      send_to_pi[0] = controller.current_total_angle[0];  // x position
      send_to_pi[1] = controller.current_total_angle[1];//controller.xy[1];  // y position
      send_to_pi[2] = volts[0]; // controller.current_velocity[0];  // x velocity
      send_to_pi[3] = volts[1]; //controller.current_velocity[1];  // y velocity
      send_to_pi[4] = current;
      send_to_pi[5] = prev_write_time-start_time;
      uint8_t msg[SEND_SIZE];
      memcpy(&msg, &send_to_pi, SEND_SIZE);
      write_to_pi(msg);
    }

  }
  else {
    write_to_motor(MOTOR_RIGHT, 0);
    write_to_motor(MOTOR_LEFT, 0);
  }

  //send_to_pi[4] = send_to_pi[0] + send_to_pi[1] + send_to_pi[2] + send_to_pi[3];  // checksum

  delayMicroseconds(150);

}

