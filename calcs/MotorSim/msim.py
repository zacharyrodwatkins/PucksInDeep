import numpy as np
import pickle
from sheets import getparams
import matplotlib.pyplot as plt
update_params = True

if update_params:
    params = dict(getparams.main())
    with open("params.pkl", "w") as f:
        pickle.dump(params, f) 

    print (params)

else:
    with open("params.pkl", "r") as f:
        params = pickle.load(f)

for key in params:
    params[key] = float(params[key])

J11 = 2*params['Large pulley MOI (kg m2)'] + params["Motor MOI (kg m^2)"] +\
      params['Small Pulley MOI (kg m2)']*params['Large Pulley Radius (m)']**2/params['Small Pulley Radius (m)']**2+\
      params['All Direction Mass']*params['Large Pulley Radius (m)']**2*1.0/2 +\
      params['Forward back mass (Diff)']*params['Large Pulley Radius (m)']**2*1.0/4

J12 = params['Small Pulley MOI (kg m2)']*params['Large Pulley Radius (m)']**2/params['Small Pulley Radius (m)']**2-params['Forward back mass (Diff)']*params['Large Pulley Radius (m)']**2/4
J = np.array(
[[J11,J12],[J12, J11]]
)

Inductance = params["Indunctane (H)"]
L = np.array(
    [[Inductance,0],[0 ,Inductance]]
)

motor_constant_k = params["K (Nm/A)"]
K = np.array(
    [[motor_constant_k,0],[0, motor_constant_k]]
)

resistance = params['Motor Resistance (Ohms)']
R = np.array([[resistance,0],[0, resistance]])

damping_factor = params['Damping Factor (Nm*s)']
B = np.array(
    [[damping_factor,0],[0,damping_factor]]
    )

# for i in [R,L,K,B]:
#     print (i)

big_ass_matrix = np.zeros((4,4))
Jinv = np.linalg.inv(J)
Linv = np.linalg.inv(L)


big_ass_matrix[0:2,0:2] = np.matmul(-Jinv,B)
big_ass_matrix[0:2,2:4] = np.matmul(Jinv, K)
big_ass_matrix[2:4, 0:2] = np.matmul(-Linv, K)
big_ass_matrix[2:4, 2:4] = np.matmul(-Linv, R)
lil_ass_matirx = np.zeros((4,4))
lil_ass_matirx[2:4, 2:4] = Linv

# print (big_ass_matrix, lil_ass_matirx)

time_steps = 1000
Total_time = 10
dt = Total_time*1.0/time_steps
T = np.linspace(0,Total_time,time_steps)
S = np.zeros((4, time_steps))
V = np.zeros((4,time_steps))
V[2,:] = np.ones(time_steps)*48
V[3,:] = np.ones(time_steps)*48

R = np.zeros((2, time_steps))
A = np.zeros((2, time_steps))
CoordsConv = params["Large Pulley Radius (m)"]/2*np.array([[1,1],[1,-1]])

for i in range(1,len(T)):
    S[:,i] = S[:,i-1] + dt*(np.matmul(big_ass_matrix,S[:,i-1]) + np.matmul(lil_ass_matirx, V[:,i-1]))
    R[:,i] = np.matmul(CoordsConv, S[0:2, i])
    A[:,i] = (R[:,i]-R[:,i-1])/dt




# print (big_ass_matrix)
# print (lil_ass_matirx)

fig, ax1 = plt.subplots()

ax2 = ax1.twinx()

# ax1.plot(T, R[0,:])
ax1.plot(T,R[0,:], color='b')
ax2.plot(T, S[3,:], color = 'r')
#ax1.plot(T, A[0,:])
ax1.set_xlabel('Time (s)')
ax1.set_ylabel('Velocity (m/s)' , color = 'b')
ax2.set_ylabel('Current (A)', color = "r")
plt.title("Velocity v.s. Time for Constant Motor Voltages")
plt.show()