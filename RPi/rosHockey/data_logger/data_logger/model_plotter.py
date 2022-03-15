import numpy as np
import matplotlib.pyplot as plt
R = 3.5306
from solve_for_coefs import get_coeffs
start = np.zeros(3)
stop = np.array([50,0,0])
Dt = 1
y_coeffs = get_coeffs(start, stop, Dt)
x_coeffs = get_coeffs(start, stop, Dt)
# x_coeffs = np.zeros(6)

#5V
A = [0.560314487219309, 5.569151280337470,  0.057975411208013]
B = [0.559703652733966,  5.561278086123814, -0.036238584630423]

# 7V (Evan March 14th mpdel)
# A = [0.900555094152792,	4.89815533615442,	0.0564943472288371]
# B =[0.899994333925378,	4.89120127441819,	-0.0463090759726549]

#10V
# A =[0.000302317987455,   0.002945831880935,   0.119058419607644]
# B =[-0.000164609682178, -0.001659107542495,  -0.002067773828908]

def get_model_function(x_coeffs, y_coeffs, t):
    theta_1_coeffs = (x_coeffs + y_coeffs)/(R)
    theta_2_coeffs = (x_coeffs - y_coeffs)/(R)
    print(theta_1_coeffs)
    print(theta_2_coeffs)
    V1 = 0
    V2 = 0
    for i in range(3):
        V1 += A[i]*np.polyval(np.polyder(theta_1_coeffs,3-i),t)+\
             B[i]*np.polyval(np.polyder(theta_2_coeffs,3-i),t)
        V2 += A[i]*np.polyval(np.polyder(theta_2_coeffs,3-i),t)+\
             B[i]*np.polyval(np.polyder(theta_1_coeffs,3-i),t)
    return np.array((V1,V2))

t = np.linspace(0,Dt)
plt.plot(t, get_model_function(x_coeffs, y_coeffs, t)[0])
plt.plot(t, get_model_function(x_coeffs, y_coeffs, t)[1])
plt.show()