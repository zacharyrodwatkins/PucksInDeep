#include <Arduino.h>
#include <RoboClaw.h>

#define MAX(x, y) (((x) > (y)) ? (x) : (y))
#define MIN(x, y) (((x) < (y)) ? (x) : (y))

class MalletController {

    float px = 55;
    float ix = 50;
    float dx = 1.2;
    float py = 45;
    float iy = 50;
    float dy = 1.35;


    int print_index = 1;

    // Size of SavGol Filter Window
    static const int window = 40;

    // make sure this value is smaller than window!!
    // Used for integrating
    static const int position_window = 500;

    float savgol[window];
    float pos_error[2][position_window] = {0};

    static HardwareSerial Serial2(PA3, PA2);
    static RoboClaw roboclaw(&Serial2, 460800);

    float result[2];
    float prev_angle[2];
    float total_angles[2];
    int crosses[2];

    float velocity[2];
    float vel_hist[2][window] = {0};
    float xy_hist[2][window] = {0};
    float time_hist[window] = {0};
    float window_step_size;

    float start_angles[2];
    float xy[2];
    float start_time;
    float des_xy[2];
    float des_vel[2];
    float int_error[2] = {0};


    float err_x;
    float err_y;
    float err_x_pos;
    float err_y_pos;
    float err_x_vel;
    float err_y_vel;

    float err_m1;
    float err_m2;

    int effort_m1;
    int effort_m2;

    void update_all_positions();
    void update_desired_path_position(float time, float x_coeffs[], float y_coeffs[], float ret_val[]);
    void write_to_motor(uint8_t address, int val);
    void readAngle(float result[]);
    void write_to_motor_simple(uint8_t val);
    void update_xy(float xy[], float total_angles[]);
    void make_total_angle(float total_angle[], float angle[], int crosses[]);
    void update_desired_path_velocity(float time, float x_coeffs[], float y_coeffs[], float ret_vel[]);
    void update_velocity(float xy[], float vel[], float xy_hist[2][window]);
    void compute_int_error();
    void savgol_coeff();
    void setPID();
    void savgol_coeff();
    void update_desired_path_position(float time, float x_coeffs[], float y_coeffs[], float ret_val[]);
    void update_desired_path_velocity(float time, float x_coeffs[], float y_coeffs[], float ret_vel[]);
    void write_to_motor(u_int8_t address, int val);
    void write_to_motor(int m1,int m2);
    void readAngle(float result[]);
    void zeroCrossing(int crosses[], float velocity[], float  angle[]);
    void make_total_angle(float total_angle[], float angle[], int crosses[]);
    void compute_int_error();


}