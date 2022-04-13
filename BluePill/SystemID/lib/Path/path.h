#include <Arduino.h>
#include <time.h>
#include <stdio.h>

typedef enum DIRECTION {
    Y=1,
    X=0
};

typedef enum FUNCTION {
    STEP = 1,
    DOUBLE_STEP = 2,
    RAMP = 3,
    TRIANGLE = 4,
    RAMP_AND_STAY = 5,
    NONE = -1
};


void ramp(DIRECTION direction, float time, float max_time, float max_v, float efforts[]){
    if (time<max_time){
        if (direction==Y){
            efforts[0] = max_v*time/max_time;
            efforts[1] = -1*efforts[0];
        }
        else {
            efforts[0] = max_v*time/max_time;
            efforts[1] = efforts[0];
        }
    }
    else {
        efforts[0]=0;
        efforts[1]=0;
    }
}
void triangle(DIRECTION direction, float time, float peak_time, float max_v, float v[]){
    float single_v;
    if (time<peak_time){
        single_v = time/peak_time*max_v;
    }
    else if (time<2*peak_time) {
        single_v = max_v-(time-peak_time)/peak_time*max_v;;
    }
    else
        single_v = 0;

    v[0]=single_v;
    if (direction==Y)
        v[1]=-v[0];
    else 
        v[1]=v[0];
}
void step(DIRECTION direction, float time, float max_time, float max_v, float v[]){
    float single_v;
    if (time<max_time){
        single_v = max_v;
    }
    else 
        single_v = 0;

    v[0]=single_v;
    if (direction==Y)
        v[1]=-v[0];
    else 
        v[1]=v[0];

}


void double_step(DIRECTION direction, float time, float peak_time, float max_v, float v[]){
    float single_v;
    if (time<peak_time){
        single_v = max_v;
    }
    else if (time<2*peak_time) 
        single_v = -max_v;

    else
        single_v = 0;

    v[0]=single_v;
    if (direction==Y)
        v[1]=-v[0];
    else 
        v[1]=v[0];
}

void ramp_and_stay(DIRECTION direction, float time, float peak_time, float max_v, float v[]){
    if (time<peak_time)
        ramp(direction, time, peak_time, max_v, v);
    else if (time<2000*peak_time)
        step(direction, 0 , peak_time, max_v, v);
    else if (time<peak_time*2005){
        float test_v[2] = {0,0};
        ramp(direction, time-2000*peak_time, peak_time*5, -max_v, test_v);
        v[0] = max_v + test_v[0];
        if (direction==Y)
            v[1] = -v[0];
        else
            v[1] = v[0];
    }
    else{
        v[0] = 0;
        v[1] = 0;
    }
}


class tester{

    public:
        tester(){
            this->function_type = NONE;
        }
        void set_function(FUNCTION function_type, DIRECTION dir, float char_time, float max_v){
            this->function_type = function_type;
            this->char_time = char_time;
            this->max_v = max_v;
            this->dir = dir;
        }        
        void get_efforts(float time, float v[]) {
            switch (this->function_type)
            {
            case STEP:
                step(this->dir, time, this->char_time, this->max_v, v);
                break;
            
            case DOUBLE_STEP:
                double_step(this->dir, time, this->char_time, this->max_v, v);
                break;

            case RAMP:
                ramp(this->dir, time, this->char_time, this->max_v, v);
                break;

            case TRIANGLE:
                triangle(this->dir, time, this->char_time, this->max_v, v);
                break;

            case RAMP_AND_STAY:
                ramp_and_stay(this->dir, time, this->char_time, this->max_v, v);
                break;


            default:
                v[0] = 0;
                v[1] = 0;
            }
        }
    
    private:
        FUNCTION function_type;
        DIRECTION dir;
        float char_time;
        float max_v;

};