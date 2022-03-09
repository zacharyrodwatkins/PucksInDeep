

class GantryModel
{
private:
    float A_step[3] = {0.00213052462653085, 0.0307510306542813, 0.132961429507223};
    float B_step[3] = {-0.00141458223317764, -0.00983851249298195, 0.0141591992993925};
    float A_dstep[3] = {0.00345334354729376, 0.00374117618306043, 0.167048868001934};
    float B_dstep[3] = {-0.00196098202412909, 0.000108006629214800, 0.0126990784212725};
    float A_ramp[3] = {0.0100122676280772, 0.0182343445428910, 0.169952418647651};
    float B_ramp[3] = {-0.00673681815835046, -0.0194725846345045, -0.0157468299246940};

    float A[3];
    float B[3];
    float* x_coeffs = {0};
    float* y_coeffs = {0};


    void get_theta(float theta_matrix[], float coeff_matrix[]);
    void get_xy_der(float t);
    
    void get_first_dir();
    void get_second_dir();
    void get_third_dir();

 

    float R = 3.5306;

public:

    enum vers { STEP = 0, DSTEP = 1, RAMP = 2 };


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

    GantryModel(int version) {
        switch (version)
        {
            case GantryModel::vers::STEP:
                for (int i=0; i<3; i++) {
                    A[i] = A_step[i];
                    B[i] = B_step[i];
                }
                break;

            case GantryModel::vers::DSTEP:
                for (int i=0; i<3; i++) {
                    A[i] = A_dstep[i];
                    B[i] = B_dstep[i];
                }
                break;

            case GantryModel::vers::RAMP:
                for (int i=0; i<3; i++) {
                    A[i] = A_ramp[i];
                    B[i] = B_ramp[i];
                }
                break;
                
            default:
                break;
        }
    }
};


