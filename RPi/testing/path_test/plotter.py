import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math

def H(t):
    return np.heaviside(t,1)


def V_exp(t):
    return 11600*H(t-1/10)/1423 - 5800*H(t)/1423 - 80600*t*H(t)/1423 + 80600*H(t-1/10)*(2*t-1/5)/1423



df = pd.read_csv("/home/ubuntu/PucksInDeep/RPi/path_test/28-01-2/run-1.txt", header=None)
print(df.head)
theta1 = list(df.iloc[:,0])
theta2 = list(df.iloc[:,1])
v1 = list(df.iloc[:,2])
v2 = list(df.iloc[:,3])
t = list(df.iloc[:,5])
print(t)
pulley_radius = 0.07115/2 

def h(t):
    if t > 0 :
        return 1
    return 0

theta_matlab = []
for i in t:
    i = i/1000
    theta_matlab.append(((800000*h(i - 1/10)*(i - 1/10)**2)/1423 - (400000*i**2*h(i))/1423)*180/math.pi)


x_exp_func = lambda t : ((4269*t**5)/80000 + (1423*t**2)/40000 + (1423*t)/40000)*100
y_exp_func = lambda t : (-(1423*t**5)/80000 + (1423*t**4)/40000 + (1423*t**3)/40000)*100



x = (np.array(theta1)+np.array(theta2))*pulley_radius/2
y = (np.array(theta1)-np.array(theta2))*pulley_radius/2

x_exp = x_exp_func(np.array(t)/1000)
y_exp = y_exp_func(np.array(t)/1000)

# V1_func = lambda t : 4269*t**5/80000 + (1423*t**2)/40000 + (1423*t)/40000
# V2_func = lambda t : -(1423*t**5)/80000 + (1423*t**4)/40000 + (1423*t**3)/40000



# plt.plot(x,y)
# plt.plot(x_exp, y_exp)
# plt.legend(["Actual Path", "Desired Path"])
# plt.xlabel("X (cm)")
# plt.ylabel("Y (cm)")
# plt.savefig("FirstModelXY-polynomial.png")


# plt.plot(t,x)
# plt.plot(t,x_exp)
# plt.plot(t,y)
# plt.plot(t,y_exp)
# plt.legend(["Actual Path", "Desired Path"])
# plt.xlabel("X (cm)")
# plt.ylabel("Y (cm)")
# plt.savefig("FirstModelXY-polynomial.png")


# plt.plot(t, theta1)
# plt.plot(t, theta2)
# plt.plot(t,theta_matlab)
# plt.plot(t, [0]*len(t))
# plt.ylabel("Degrees")
plt.plot(t, v1)
plt.plot(t, v2)
# plt.plot(t, V_exp(np.array(t)/1000))
# print(V_exp(np.array(t)))
# plt.legend(["theta1 measured", "theta2 measured", "theta1 expected", "theta2 expected"])
# plt.xlabel("Time (ms)")
# plt.savefig("FirstModelTest.png")


plt.show()

