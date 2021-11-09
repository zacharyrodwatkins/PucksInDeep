#include <Arduino.h>
#include <SPI.h>
#include "RoboClaw.h"
// #include <time.h>
#define CHIP_SELECT_LEFT A4
#define CHIP_SELECT_RIGHT PB5
#define MOTOR_LEFT 0x81
#define MOTOR_RIGHT 0x80
#define two_to_the_14 16384
#define PULLEY_RADIUS 7.0612 // 2.78 inches in cm
#define ANGLE_THRESH 350
#define NUM_READS 200
// #define SIMPLE_H
#define OMEGA 360.0
float ticks_to_deg = 360.0/two_to_the_14;
int j = 0;
int k = 0;

float test_path_straight_y[6] ={180,-450, 300,0,0,0};
float test_path_straight_x[6] = {0,0,0,0,0,0};


#define MAX(x, y) (((x) > (y)) ? (x) : (y))
#define MIN(x, y) (((x) < (y)) ? (x) : (y))

HardwareSerial Serial2(PA3, PA2);
RoboClaw roboclaw(&Serial2,460800);

u_int16_t result[2];
u_int16_t prev_angle[2];
float total_angles[2];
int crosses[2];

int prev_time[2];
float velocity[2];
float start_angles[2];
float xy[2];
float start_time;
float des_xy[2];
float current_time;
float err_x;
float err_y;
float right_motor_effort;
float left_motor_effort;
float p = 69.0;

void update_desired_path_position(float time, float x_coeffs[], float y_coeffs[], float ret_val[]);
void write_to_motor(uint8_t address, int val);
void readAngle(u_int16_t result[]);
void write_to_motor_simple(uint8_t val);
void update_xy(float xy[], float total_angles[]);

void setup() {
  pinMode(CHIP_SELECT_LEFT, OUTPUT);
  pinMode(CHIP_SELECT_RIGHT, OUTPUT);
  digitalWrite(CHIP_SELECT_LEFT, HIGH);
  digitalWrite(CHIP_SELECT_RIGHT, HIGH);
  Serial.begin(9600);
  Serial2.begin(460800);
  SPI.beginTransaction(SPISettings(115200, MSBFIRST, SPI_MODE1));
  readAngle(result);

  for (int i=0;i<2;i++){
    start_angles[i] = result[i]*ticks_to_deg;
  }

  update_xy(xy,start_angles);
  delay(10);
  start_time = micros()*1e-6;
}

void update_xy(float xy[], float total_angles[]){
  xy[0] = (total_angles[0]+total_angles[1])/2*PULLEY_RADIUS;
  xy[1] = (total_angles[0]-total_angles[1])/2*PULLEY_RADIUS;
}


void update_desired_path_position(float time, float x_coeffs[], float y_coeffs[], float ret_val[]){
  ret_val[0] = 0;
  ret_val[1] = 0;
  float tpow = 1;
  for (int i = 5; i>=0; i--){
    ret_val[0] += x_coeffs[i]*tpow;
    ret_val[1] += y_coeffs[i]*tpow;
    tpow *= time;
  }
}



void write_to_motor(u_int8_t address, int val){
  if (val<0){roboclaw.ForwardM1(address ,(uint8_t) val);
    val = MAX(val,-127);
    roboclaw.BackwardM1(address, (uint8_t) abs(val));
  }
  else {
    val = MIN(val,127);
    roboclaw.ForwardM1(address ,(uint8_t) val);
  }
}


//Read from or write to register from the SCP1000:
void readAngle(u_int16_t result[]) {
  int chips[2] = {CHIP_SELECT_LEFT,CHIP_SELECT_RIGHT};
  
  for (int i = 0; i<2; i++) {
    u_int16_t reads; // incoming byte from the SPI
    digitalWrite(chips[i], LOW);
    reads = SPI.transfer16(0xFF);
    digitalWrite(chips[i],HIGH);
    result[i] = (reads & 0b0011111111111111)*ticks_to_deg;
    }

}



  void zeroCrossing(int crosses[], float velocity[]){
    for (int i=0; i<2; i++) {
      if ((result[i] - prev_angle[i]) > ANGLE_THRESH) {
          crosses[i] += 1;
          int time = micros();
          velocity[i] = 1000000/(time - prev_time[i]);
          prev_time[i] = time;
        }
        else if ((-result[i] + prev_angle[i]) > ANGLE_THRESH){
          crosses[i] -= 1;
        }
        prev_angle[i] = result[i];
      }
  }


void make_total_angle(float total_angle[], uint16_t angle[], int crosses[]){
  for (int i=0;i<2;i++){
    total_angle[i] = ticks_to_deg*total_angle[i]+crosses[i]*360.0;
  }
}




void loop() {

  readAngle(result);
  zeroCrossing(crosses,velocity);
  make_total_angle(total_angles,result,crosses);
  current_time = micros()*1e-6-start_time;
  update_desired_path_position(current_time, test_path_straight_x,test_path_straight_y,des_xy);
  update_xy(xy,total_angles);
  err_x = -1*(xy[0]-des_xy[0]);
  err_y = -1*(xy[1]-des_xy[1]);
  float err_m1 = (err_x+err_y)/PULLEY_RADIUS;
  float err_m2 = (err_x-err_y)/PULLEY_RADIUS;
  write_to_motor(MOTOR_RIGHT, (uint8_t) err_m1*p);
  write_to_motor(MOTOR_LEFT, (uint8_t) err_m2*p);
}