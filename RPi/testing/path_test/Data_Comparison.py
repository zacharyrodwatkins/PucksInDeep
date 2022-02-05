import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math



df = pd.read_csv("/home/ubuntu/PucksInDeep/RPi/testing/path_test/2022-02-02/run-1.txt", header=1)
print(df.head)
X = list(df.iloc[:,0])
Y = list(df.iloc[:,1])
VX = list(df.iloc[:,2])
VY = list(df.iloc[:,3])
t = list(df.iloc[:,4])
print(t)

def make_theoretical_curves(t,xcoefs,ycoefs):
    x,y,vx,vy = [],[],[],[]
    for i in t:
        xnew,ynew,vxnew,vynew = 0,0,0,0
        for j in range(len(xcoefs)):
            p = 5
            a,b = xcoefs[j],ycoefs[j]
            xnew += a*(i**p)
            ynew += b*(i**p)
            p -=1
            if p >= 0:
                vxnew += (p+1)*a*(i**p)
                vynew += (p+1)*b*(i**p)
        x.append(xnew)
        y.append(ynew)
        vx.append(vxnew)
        vy.append(vynew)
    return x,y,vx,vy

Xcoefs, Ycoefs = [2400.0,-6000.0,4000.0,0.0,0.0,0.0], [2400.0,-6000.0,4000.0,0.0,0.0,0.0]
t = np.array(t)
X_th, Y_th, VX_th, VY_th = make_theoretical_curves((t-t[0])/1e3,Xcoefs,Ycoefs)

plt.plot((t-t[0])/1e3,X,color="b")
plt.plot((t-t[0])/1e3,X_th,color="r")

plt.plot((t-t[0])/1e3,Y,color="g")
plt.plot((t-t[0])/1e3,Y_th,color="purple")

plt.show()