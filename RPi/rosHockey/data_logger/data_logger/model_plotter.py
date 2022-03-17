import numpy as np
import matplotlib.pyplot as plt
R = 3.5306

# # 5V
# A = [0.560314487219309, 5.569151280337470,  0.057975411208013]
# B = [0.559703652733966,  5.561278086123814, -0.036238584630423]

# #10V
# A = [0.900555094152792,	4.89815533615442,	0.0564943472288371]
# B =[0.899994333925378,	4.89120127441819,	-0.0463090759726549]

A =[0.000302317987455,   0.002945831880935,   0.119058419607644]
B =[-0.000164609682178, -0.001659107542495,  -0.002067773828908]




def get_model_function(x_coeffs, y_coeffs):
    theta_1_coeffs = (x_coeffs + y_coeffs)/(R)
    theta_2_coeffs = (x_coeffs - y_coeffs)/(R)
    V1 = 0
    V2 = 0


    for i in range(3):
        dir_vec_1 = np.zeros(6)
        dir_vec_1[0:6-3+i] = np.polyder(theta_1_coeffs,3-i)
        dir_vec_2 = np.zeros(6)
        dir_vec_2[0:6-3+i] = np.polyder(theta_2_coeffs,3-i)
        V1 += A[i]*dir_vec_1+\
             B[i]*dir_vec_2
        V2 += A[i]*dir_vec_2+\
             B[i]*dir_vec_1

    func = lambda t :(np.polyval(V1,t),np.polyval(V2,t))

    return func


if __name__ == "__main__":
    from solve_for_coefs import get_coeffs
    start = np.zeros(3)
    stop = np.array([75,0,0])
    Dt = 1
    y_coeffs = get_coeffs(start, stop, Dt)
    x_coeffs = np.zeros(6)
    t = np.linspace(0,Dt)
    plt.plot(t, get_model_function(x_coeffs, y_coeffs, t)[0])
    plt.plot(t, get_model_function(x_coeffs, y_coeffs, t)[1])
    plt.show()
