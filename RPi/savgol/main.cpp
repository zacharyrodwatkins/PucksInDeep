#include "savgol.hpp"
#include <stdio.h>
#include <unistd.h>


// to remake a lib do cmake .
// to recompile type in make
// to run type in ./main

SavitskyGolay savgol;

int main(void){

    savgol.Constructor();

    float xy[] = {0.0,0.0};

    for(int i = 0; i<500; i++){
        xy[0] += 1000000;
        xy[1] += 2000;
        savgol.update_velocity(xy);
        printf("\n Vel %d \n", i);
        printf("%f \n", savgol.vel[0]);
        printf("%f \n", savgol.vel[1]);
        printf("%f \n", xy[0]);


        usleep(30000);

    }

    return 0;
}