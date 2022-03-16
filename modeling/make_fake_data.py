# generate fake voltage data from a model
import re
import numpy as np

A = [0.00065, 0.00725, 0.10075]
B = [-0.00035, -0.00315,  0.00285]

M = np.array([[A,B],[B,A]])


def make_dir_matrix(degree,order=1):
    if (order == 0):
        return np.eye(degree+1,degree+1)

    M = np.zeros((degree+1,degree+1))
    for i in range(1,degree+1):
        M[i,i-1] = degree+1-i
    return np.matmul(M,make_dir_matrix(degree, order-1))

