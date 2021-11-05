#include <Arduino.h>
#include <SPI.h>
#include "RoboClaw.h"
// #include <time.h>
#define CHIP_SELECT_LEFT A4
#define CHIP_SELECT_RIGHT PB5
#define MOTOR_LEFT 0x8
#define MOTOR_RIGHT 0x80
#define two_to_the_14 16384
#define ANGLE_THRESH 350
#define NUM_READS 200
// #define SIMPLE_H
#define OMEGA 360.0
float ticks_to_deg = 360.0/two_to_the_14;
int j = 0;
int k = 0;


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
bool direction = 0;

// uint32_t before;
// uint32_t after;
int before;
int after;
int msecs[NUM_READS];


void write_to_motor(uint8_t address, int val);
void readAngle(u_int16_t result[]);
void write_to_motor_simple(uint8_t val);

void setup() {
  // delay(1000);
  pinMode(CHIP_SELECT_LEFT, OUTPUT);
  pinMode(CHIP_SELECT_RIGHT, OUTPUT);
  digitalWrite(CHIP_SELECT_LEFT, HIGH);
  digitalWrite(CHIP_SELECT_RIGHT, HIGH);
  Serial.begin(9600);
  Serial2.begin(460800);
  SPI.beginTransaction(SPISettings(115200, MSBFIRST, SPI_MODE1));
  // // roboclaw.begin(38400); 
  readAngle(result);

  for (int i=0;i<2;i++){
    start_angles[i] = result[i]*ticks_to_deg;
  }
  delay(10);
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

void display(void){
    Serial.print("Left motor values: ");
    Serial.print(crosses[0]);
    Serial.print(" ");
    Serial.print(result[0]);
    Serial.print(" ");
    Serial.print(velocity[0]);
    Serial.print("\n");

    Serial.print("Right motor values: ");
    Serial.print(crosses[1]);
    Serial.print(" ");
    Serial.print(result[1]);
    Serial.print(" ");
    Serial.print(velocity[1]);
    Serial.print("\n");
}

void make_total_angle(float total_angle[], uint16_t angle[], int crosses[]){
  for (int i=0;i<2;i++){
    total_angle[i] = ticks_to_deg*total_angle[i]+crosses[i]*360.0;
  }
}

void write_to_motor_simple(uint8_t val){
  Serial2.write(val);
}



void loop() {

  readAngle(result);
  zeroCrossing(crosses,velocity);
  make_total_angle(total_angles,result,crosses);
if (total_angles[1]<start_angles[1]+360){
    before = micros();
    write_to_motor(MOTOR_RIGHT, 100);

    after = micros();
}
else{
   write_to_motor(MOTOR_RIGHT, -50);
   delay(1000000);
}

  //  
  // zeroCrossing(crosses, velocity);
  // write_to_motor()

  // if (true){
  //   Serial.print(total_angles[1]);
  // }

  // if (j % 50000 == 0){
  //   Serial.print("Left motor values: ");
  //   Serial.print(crosses[0]);
  //   Serial.print(" ");
  //   Serial.print(result[0]);
  //   Serial.print(" ");
  //   Serial.print(velocity[0]);
  //   Serial.print("\n");

  //   Serial.print("Right motor values: ");
  //   Serial.print(crosses[1]);
  //   Serial.print(" ");
  //   Serial.print(result[1]);
  //   Serial.print(" ");
  //   Serial.print(velocity[1]);
  //   Serial.print("\n");
  // }
}