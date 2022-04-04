#include "savgol.hpp"
#include "chrono"
#include "ctime"
#include <stdint.h>
#include <inttypes.h>

void SavitskyGolay::update_velocity(float xy[]) {
  printf("\n Time \n");

  printf("%" PRIu64 "\n", micros());
  float time_on_path = micros()-start_time;
  for(int i=window-1;i>0;i--){
    time_hist[i] = time_hist[i-1];
  }

  time_hist[0] = ((float) time_on_path)*1e-6;
  window_step_size = (time_hist[0] - time_hist[window-1])/(window-1);
  printf("\n Window Size \n");
  printf("%f \n", window_step_size);



  for(int i=window-1;i>0;i--){
    xy_hist[0][i] = xy_hist[0][i-1];
    xy_hist[1][i] = xy_hist[1][i-1];
  }
  xy_hist[0][0] = xy[0];
  xy_hist[1][0] = xy[1];

  float sum_vel[2] = {0,0};

  for (int i = 0;i<2;i++){
    for (int j = 0; j < window;j++){
      sum_vel[i] += xy_hist[i][j]*savgol[j];
    }
  }
  vel[0] = sum_vel[0]/(window_step_size);
  vel[1] = sum_vel[1]/(window_step_size);

}

uint64_t SavitskyGolay::micros()
{
    uint64_t us = std::chrono::duration_cast<std::chrono::microseconds>(
            std::chrono::high_resolution_clock::now().time_since_epoch())
            .count();
    return us; 
}