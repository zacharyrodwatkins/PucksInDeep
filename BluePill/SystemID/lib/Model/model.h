

class GantryModel
{
private:

    float A[3] = {0.00065, 0.00725, 0.10075};
    float B[3] = {-0.00035, -0.00315,  0.00285};
    float* x_coeffs = {0};
    float* y_coeffs = {0};


    void get_theta(float theta_matrix[], float coeff_matrix[]);
    void get_xy_der(float t);
    
    void get_first_dir();
    void get_second_dir();
    void get_third_dir();

 

    float R = 3.5306;

public:

    float theta[2] = {0};
    float theta1[2] = {0};
    float theta2[2] = {0};
    float theta3[2] = {0};

    float xy[6][2] = {0};
    float xy1[2] = {0};
    float xy2[2] = {0};
    float xy3[2] = {0};


    void set_coeffs(float* x_coeffs, float* y_coeffs);
    float* get_effort(float time);
};


