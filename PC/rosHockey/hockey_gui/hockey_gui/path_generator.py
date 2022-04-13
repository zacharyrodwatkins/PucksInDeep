import numpy as np
import matplotlib.pyplot as plt
from numpy.lib.twodim_base import vander
time = 1
y_start = np.array([0,0,0])
y_end = np.array([30,0,0])
x_start = np.array([0,0,0])
x_end = np.array([30,0,0])


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

def gen_path(x_start, y_start, x_end, y_end, time):
    t = np.linspace(0,time)
    y_coeffs = get_coeffs(y_start,y_end, 1)
    y = np.matmul(vander(t,6),y_coeffs)
    x_coeffs = get_coeffs(x_start,x_end, 1)
    x = np.matmul(vander(t,6),x_coeffs)
    print("Generated path")
    return (x, y, t)