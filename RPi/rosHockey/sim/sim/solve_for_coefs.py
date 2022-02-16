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

def get_all_functions(startx,stopx,starty,stopy, dt):
    coeffsx = get_coeffs(startx,stopx,dt)
    coeffsy = get_coeffs(starty,stopy)
    funcs = [[get_function(coeffsx,dt), get_function(coeffsy,dt)],
        [get_derivative_function(coeffsx,dt), get_derivative_function(coeffsy,dt)],
        [get_2nd_derivative_function(coeffsx,dt), get_2nd_derivative_function(coeffsy,dt)]]

    return lambda t : np.array([[funcs[i,j](t) for j in range(2)] for i in range(3)])

def get_function(coeffs,dt):
    return lambda t : np.dot(coeffs, np.vander(np.array([t]),6)[0]) if t < dt\
        else lambda t : np.dot(coeffs, np.vander(np.array([dt]),6)[0])

def get_derivative_function(coeffs, dt):
    return lambda t : np.dot(coeffs, np.array(5,4,3,2,1,0)/t*np.vander(np.array([t]),6)[0]) if t < dt else 0

def get_2nd_derivative_function(coeffs, dt):
    return lambda t : np.dot(coeffs, np.array(5*4,4*3,3*2,2,0,0)/t**2*np.vander(np.array([t]),6)[0]) if t < dt else 0

