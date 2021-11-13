#include <Arduino.h>
#include <SPI.h>
#include "RoboClaw.h"
// #include <time.h>
#define CHIP_SELECT_LEFT A4
#define CHIP_SELECT_RIGHT PB5
#define MOTOR_LEFT 0x81
#define MOTOR_RIGHT 0x80
#define two_to_the_14 16384
#define PULLEY_RADIUS 3.5306 // 2.78 inches in cm
#define ANGLE_THRESH 350
#define NUM_READS 200
// #define SIMPLE_H
#define OMEGA 360.0
float ticks_to_deg = 360.0/two_to_the_14;
float mm_to_g = 1;
int j = 0;
int k = 0;
int print_index = 1;
int speed = 0;

float savgol[13] = {0.03297,0.02747,0.02198,0.01648,0.01099,0.00549,0,-0.00549,-0.01099,-0.01648,-0.02198,-0.02747,-0.03297};

// [ 360. -900.  600.    0.    0.    0.]
float test_path_straight_y[6] ={2*360,-2*900, 2*600,0,0,0};
float test_path_straight_x[6] = {0,0,0,0,0,0};


#define MAX(x, y) (((x) > (y)) ? (x) : (y))
#define MIN(x, y) (((x) < (y)) ? (x) : (y))

HardwareSerial Serial2(PA3, PA2);
RoboClaw roboclaw(&Serial2,460800);

float result[2];
float prev_angle[2];
float total_angles[2];
int crosses[2];

float prev_time = 0;
float time_diff = 1;
float acc[2] = {0};
float velocity[2];
float prev_vel[2] = {0,0};
float vel_hist[2][13] = {0};
float xy_hist[2][13] = {0};
float start_angles[2];
float xy[2];
float prev_xy[2];
float start_time;
float des_xy[2];
float des_vel[2];
float des_acc[2];
float current_time;
float err_x;
float err_y;

float d = 1;
float p = 0.5;
float a = 0.2;
float err_m1;
float err_m2;

float y_test[1000];
float t_test[1000];


void update_desired_path_position(float time, float x_coeffs[], float y_coeffs[], float ret_val[]);
void write_to_motor(uint8_t address, int val);
void readAngle(float result[]);
void write_to_motor_simple(uint8_t val);
void update_xy(float xy[], float total_angles[]);
void make_total_angle(float total_angle[], float angle[], int crosses[]);
void update_desired_path_velocity(float time, float x_coeffs[], float y_coeffs[], float ret_vel[]);
void update_acceleration(float vel_hist[2][13], float acc[]);
void update_velocity(float xy[], float vel[], float acc[], float xy_hist[2][13]);

void setup() {
  pinMode(CHIP_SELECT_LEFT, OUTPUT);
  pinMode(CHIP_SELECT_RIGHT, OUTPUT);
  digitalWrite(CHIP_SELECT_LEFT, HIGH);
  digitalWrite(CHIP_SELECT_RIGHT, HIGH);
  Serial.begin(9600);
  Serial2.begin(460800);
  SPI.beginTransaction(SPISettings(115200, MSBFIRST, SPI_MODE1));
  readAngle(result);
  make_total_angle(total_angles, result, crosses);

  for (int i=0;i<2;i++){
    start_angles[i] = result[i];
  }

  delay(10);
  start_time = micros()*1e-6;
  prev_time = start_time;

}

void update_xy(float xy[], float total_angles[]){  
  xy[0] = (total_angles[0]+total_angles[1])/2*PULLEY_RADIUS*PI/180;
  xy[1] = (total_angles[0]-total_angles[1])/2*PULLEY_RADIUS*PI/180;

  for(int i=12;i>0;i--){
    xy_hist[0][i] = xy_hist[0][i-1];
    xy_hist[1][i] = xy_hist[1][i-1];
  }
  xy_hist[0][0] = xy[0];
  xy_hist[1][0] = xy[1];
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

void update_desired_path_velocity(float time, float x_coeffs[], float y_coeffs[], float ret_vel[]){
  ret_vel[0] = 0;
  ret_vel[1] = 0;
  float tpow = 1;
  for (int i = 4; i>=0; i--){
    ret_vel[0] += x_coeffs[i]*tpow*(4-i+1);
    ret_vel[1] += y_coeffs[i]*tpow*(4-i+1);
    tpow *= time;
  }
}

void update_desired_path_acc(float time, float x_coeffs[], float y_coeffs[], float ret_acc[]){
  ret_acc[0] = 0;
  ret_acc[1] = 0;
  float tpow = 1;
  for (int i = 3; i>=0; i--){
    ret_acc[0] += x_coeffs[i]*tpow*(4-i+1)*(3-i+1);
    ret_acc[1] += y_coeffs[i]*tpow*(4-i+1)*(3-i+1);
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
void readAngle(float result[]) {
  int chips[2] = {CHIP_SELECT_LEFT,CHIP_SELECT_RIGHT};
  
  for (int i = 0; i<2; i++) {
    u_int16_t reads; // incoming byte from the SPI
    digitalWrite(chips[i], LOW);
    reads = SPI.transfer16(0xFF);
    digitalWrite(chips[i],HIGH);
    result[i] = 360.0-(reads & 0b0011111111111111)*ticks_to_deg-start_angles[i];
    }

}

void zeroCrossing(int crosses[], float velocity[], float  angle[]){
    for (int i=0; i<2; i++) {
      if ((angle[i] - prev_angle[i]) > ANGLE_THRESH) {
          crosses[i] -= 1;
        }
        else if ((-result[i] + prev_angle[i]) > ANGLE_THRESH){
          crosses[i] += 1;
        }
        prev_angle[i] = result[i];
      }
  }

void make_total_angle(float total_angle[], float angle[], int crosses[]){
  for (int i=0;i<2;i++){
    total_angle[i] = angle[i]+crosses[i]*360.0;
  }
}

void update_acceleration(float vel[2][13], float acc[]){
  float sum_acc[2] = {0};
  for (int i = 0;i<2;i++){
    for (int j = 0; j < 13;j++){
      sum_acc[i] = sum_acc[i] + vel[i][j]*savgol[j];
  }
  }
  acc[0] = sum_acc[0]/(time_diff*mm_to_g);
  acc[1] = sum_acc[1]/(time_diff*mm_to_g);

}
void update_velocity(float xy[], float vel[], float acc[], float xy_hist[2][13]){
  float time_secs = micros()*1e-6-start_time;
  time_diff = time_secs-prev_time;
  // Serial.println();
  // Serial.print((vel[0]));
  // Serial.print(" ");
  // Serial.print(prev_vel[0]);
  // Serial.println();
  float sum_vel[2] = {0};
  for (int i = 0;i<2;i++){
    for (int j = 0; j < 13;j++){
      sum_vel[i] = sum_vel[i] + xy_hist[i][j]*savgol[j];
  }
  }
  vel[0] = sum_vel[0]/(time_diff);
  vel[1] = sum_vel[1]/(time_diff);


// old velocity calculation
  // vel[0] = (xy[0]-prev_xy[0])/(time_diff);
  // vel[1] = (xy[1]-prev_xy[1])/(time_diff);



  for(int i=12;i>0;i--){
    vel_hist[0][i] = vel_hist[0][i-1];
    vel_hist[1][i] = vel_hist[1][i-1];
  }


  vel_hist[0][0] = vel[0];
  vel_hist[1][0] = vel[1];

  prev_vel[0] = vel[0];
  prev_vel[1] = vel[1];

  prev_xy[0] = xy[0];
  prev_xy[1] = xy[1];
  prev_time = time_secs;
}

float xy_to_m1(float err_x, float err_y){
  return (err_x + err_y)/PULLEY_RADIUS;
}

float xy_to_m2(float err_x, float err_y){
  return (err_x - err_y)/PULLEY_RADIUS;
}

void loop() {

  readAngle(result);
  zeroCrossing(crosses,velocity, result);
  make_total_angle(total_angles,result,crosses);
  current_time = micros()*1e-6-start_time;
  

  if (current_time>1){
    write_to_motor(MOTOR_LEFT, 0);
    write_to_motor(MOTOR_RIGHT,0);
    Serial.println("DONE");
    Serial.print(err_x);
    Serial.print(" ");
    Serial.print(err_y);
    Serial.print(" ");
    Serial.print(err_m1);
    Serial.print(" ");
    Serial.print(err_m2);
    Serial.print(" ");
    Serial.print(current_time);
    Serial.println();
    while (true)
    {
      /* code */
    }
  }


  update_xy(xy,total_angles);
  if (print_index>13){
    update_acceleration(vel_hist,acc);
    update_velocity(xy, velocity,acc,xy_hist);
  }
  update_desired_path_velocity(current_time, test_path_straight_x, test_path_straight_y, des_vel);
  update_desired_path_position(current_time, test_path_straight_x,test_path_straight_y,des_xy);
  update_desired_path_acc(current_time, test_path_straight_x, test_path_straight_y, des_acc);


  err_x = (des_xy[0]-xy[0]);
  err_y = (des_xy[1]-xy[1]);
  float err_x_vel = (des_vel[0]-velocity[0]);
  float err_y_vel = (des_vel[1]-velocity[1]);
  float err_x_acc = (des_acc[0]-acc[0]);
  float err_y_acc = (des_acc[1]-acc[1]);

  // if (print_index % 1000 == 0){

  //   Serial.print(err_x);
  //   Serial.print(" ");
  //   Serial.print(err_y);
  //   Serial.print(" ");
  //   Serial.print(current_time);
  //   Serial.println();

  // }

  float err_m1_vel = (err_x_vel+err_y_vel)/PULLEY_RADIUS;
  float err_m2_vel = (err_x_vel-err_y_vel)/PULLEY_RADIUS;
  err_m1 = (err_x+err_y)/PULLEY_RADIUS;
  err_m2 = (err_x-err_y)/PULLEY_RADIUS;

  float err_m1_acc = xy_to_m1(err_x_acc,err_y_acc);
  float err_m2_acc = xy_to_m2(err_x_acc,err_y_acc);

  int effort_m1 =  (err_m1*p+d*err_m1_vel+a*err_m1_acc);
  int effort_m2 = (err_m2*p+d*err_m2_vel+a*err_m2_acc);
  write_to_motor(MOTOR_LEFT, effort_m1);
  write_to_motor(MOTOR_RIGHT, effort_m2);
  
  // write_to_motor(MOTOR_LEFT, 50);
  // write_to_motor(MOTOR_RIGHT, 50);
  
  // if (print_index%100==0){
  //   speed++;
  //   int pos_speed = speed%100;
  //   int neg_speed = -1*pos_speed;
  //   // Serial.println(pos_speed);
  //   write_to_motor(MOTOR_LEFT, pos_speed);
  //   write_to_motor(MOTOR_RIGHT, neg_speed);
  // }

  print_index ++;

  if (print_index % 1 == 0){

    // Serial.print(des_vel[0]);
    // Serial.print(" ");
    // Serial.println("here is vel");
    // Serial.print(velocity[0]);
    // Serial.print(" ");
    // Serial.print(des_vel[1]);
    // Serial.print(" ");
    // Serial.print(velocity[1]);
    // Serial.print(" ");
    // Serial.print(err_y_vel);
    // Serial.print(" ");
    // Serial.print(effort_m1);
    // Serial.print(" ");
    // Serial.print(effort_m2);
    Serial.print(des_acc[0]);
    Serial.print(" ");
    Serial.print(des_acc[1]);
    Serial.print(" ");
    Serial.println("Here is acc  ");
    Serial.print(acc[0]);
    Serial.print(" ");
    Serial.println(acc[1]);
    // Serial.println("Here is the vel hist");
    // for (int i = 0;i<13;i++){
    //     Serial.print(vel_hist[0][i]);
    //     Serial.print(" ");
    // }


    

    Serial.println();

  }
  delayMicroseconds(150);


}