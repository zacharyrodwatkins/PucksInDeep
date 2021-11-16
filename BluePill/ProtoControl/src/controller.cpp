#include <Arduino.h>
#include <RoboClaw.h>
#include "MalletController.h"

#define MAX(x, y) (((x) > (y)) ? (x) : (y))
#define MIN(x, y) (((x) < (y)) ? (x) : (y))


void MalletController::update_desired_path_position(float time, float x_coeffs[], float y_coeffs[], float ret_val[]){
  ret_val[0] = 0;
  ret_val[1] = 0;
  float tpow = 1;
  for (int i = 5; i>=0; i--){
    ret_val[0] += x_coeffs[i]*tpow;
    ret_val[1] += y_coeffs[i]*tpow;
    tpow *= time;
  }
}

void MalletController::update_desired_path_velocity(float time, float x_coeffs[], float y_coeffs[], float ret_vel[]){
  ret_vel[0] = 0;
  ret_vel[1] = 0;
  float tpow = 1;
  for (int i = 4; i>=0; i--){
    ret_vel[0] += x_coeffs[i]*tpow*(4-i+1);
    ret_vel[1] += y_coeffs[i]*tpow*(4-i+1);
    tpow *= time;
  }
}

void MalletController::write_to_motor(u_int8_t address, int val){
  if (val<0){MalletController::roboclaw.ForwardM1(address ,(uint8_t) val);
    val = MAX(val,-127);
    MalletController::roboclaw.BackwardM1(address, (uint8_t) abs(val));
  }
  else {
    val = MIN(val,127);
    MalletController::roboclaw.ForwardM1(address ,(uint8_t) val);
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

void MalletController::zeroCrossing(int crosses[], float velocity[], float  angle[]){
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

void MalletController::make_total_angle(float total_angle[], float angle[], int crosses[]){
  for (int i=0;i<2;i++){
    total_angle[i] = angle[i]+crosses[i]*360.0;
  }
}

void MalletController::compute_int_error(){
    for (int i = 0; i<2; i++) {
      // subtract off the last value from mean
      int_error[i] = int_error[i] - pos_error[i][position_window -1]/position_window;
    }
    
    for(int i=position_window-1;i>0;i--){
    pos_error[0][i] = pos_error[0][i-1];
    pos_error[1][i] = pos_error[1][i-1];
  }

    // calculate the new error
    for(int i = 0; i<2; i++){
       pos_error[i][0] = des_xy[i]-xy[i];
    }

    for(int i = 0; i<2; i++){
       int_error[i] = int_error[i]+pos_error[i][0]/position_window;
    }
}

void MalletController::update_velocity(float xy[], float vel[], float xy_hist[2][window]){
  float sum_vel[2] = {0};
  for (int i = 0;i<2;i++){
    for (int j = 0; j < window;j++){
      sum_vel[i] = sum_vel[i] + xy_hist[i][j]*savgol[j];
  }
  }

  vel[0] = sum_vel[0]/(window_step_size);
  vel[1] = sum_vel[1]/(window_step_size);


  for(int i=window-1;i>0;i--){
    vel_hist[0][i] = vel_hist[0][i-1];
    vel_hist[1][i] = vel_hist[1][i-1];
  }


  vel_hist[0][0] = vel[0];
  vel_hist[1][0] = vel[1];

}