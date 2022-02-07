import numpy as np
import matplotlib.pyplot as plt
from numpy.lib.twodim_base import vander
time = 0.5
start = np.array([0,0,0])
end = np.array([50,0,-1000])


def get_coeffs(start, stop, Dt):
    mat = gen_mat(Dt)
    s = np.zeros(6)
    s[:3] = start 
    s[3:] = stop
    return np.linalg.solve(mat,s)


def gen_mat(Dt):
    T= np.vander(np.array([Dt]),6)[0]
    mat = np.zeros((6,6))
    mat[:3,3:] = np.array([[0,0,1],[0,1,0],[2,0,0]])
    mat[3] = T
    mat[4,:-1] = np.array([5,4,3,2,1])*T[1:]+np.array([0,0,0,0,1])
    mat[5,:-2] = T[2:]*np.array([20,12,6,0]) + np.array([0,0,0,2])
    return mat

coeffs = get_coeffs(start,end, time)
t = np.linspace(0,time+0.1)
# t = vander(t,6).shape
# print(t)
y = np.matmul(vander(t,6),coeffs)
plt.plot(t,y)
plt.show()
print(coeffs)