#define window 5
#include <stdio.h>
#include "time.h"
#include <stdint.h>
 
class SavitskyGolay {
    public:
        //Coefficients for savgol filter

        float savgol[window] = {};
        float vel[2] = {0,0};
        float xy_hist[2][window] = {0,0};
        float time_hist[window] = {0,0};
        float window_step_size;
        uint64_t micros();

        uint64_t start_time = 1.0*micros();

    private:

        void update_savgol_coeff(float coeffs[]){
            float start = 6.0/(window*1.0*(window+1));
            float del = -12.0/(1.0*(window-1)*(window)*(window+1));

            for (int i = 0; i<window; i++){
                coeffs[i] = start;
                start = start+del;
                printf("\n Coeff %d \n", i);
                printf("%f \n", coeffs[i]);

            }
        }
        
        
        
    public:

        void Constructor() {
            vel[0] = 1;
            //Coefficients for savgol filter, set window in definition
            update_savgol_coeff(savgol);
        }

    void update_velocity(float xy[]);
    void test();
    


};