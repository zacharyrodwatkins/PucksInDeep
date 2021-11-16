import numpy as np
import matplotlib.pyplot as plt
from numpy.lib.twodim_base import vander
t = np.array([0,1/6,2/6,3/6,4/6,5/6,1])
A = vander(t,6)
X = np.array([0,1,-1,1,-1,0])
Y = np.array([0,1,1,-1,-1,0])
print(A.shape,X.shape)
cx = np.linalg.solve(A,X)
cy = np.linalg.solve(A,Y)
print(cx,cy)
T = np.linspace(0,1,100)
Tarr = vander(T,6)
y = np.matmul(Tarr,cy)
x = np.matmul(Tarr,cx)
plt.plot(T,y)
plt.plot(T,x)
plt.show()