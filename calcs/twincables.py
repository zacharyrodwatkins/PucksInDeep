import numpy as np 
import math
from scipy.optimize import fsolve

pi = math.pi
alpha = 5.0/180*pi #rad
l = 1.22  # m
lc = l/math.cos(alpha) # m
h = math.sin(alpha)*lc # m 
cable_diameter = 1.0/16*25.4/1000 # m 
rod_od =  0.5 * 25.4/1000 # m 
rod_id = 0.43 * 25.4/1000 # m
rod_area = pi*(rod_od**2- rod_id**2)/4
cable_area = pi*cable_diameter**2/4
cable_young_modulus = 200e6 # kpa 
rod_young_modulus = 69e6 # kpa
Tension = 62e-3 # kn

get_dlc = lambda delta : math.sqrt(l**2+(h+delta)**2) - lc
get_dlrod = lambda delta : math.sqrt(l**2+delta**2)-l

get_Flc = lambda delta :cable_area * cable_young_modulus * get_dlc(delta)/lc # kn
get_Frod = lambda delta : rod_area * rod_young_modulus * get_dlrod(delta)/l # kn
get_sin_deflection_angle = lambda delta :  delta / math.sqrt(l**2 + delta **2)

# x is a list of flc,frod,delta

cable_compatability = lambda x : x[0] - get_Flc(x[2])
rod_compatability = lambda x: x[1] - get_Frod(x[2])
force_balance = lambda x : x[1] * get_sin_deflection_angle(x[2]) + 2*x[0]*(h+x[2])/math.sqrt(l**2 + (h+x[2])**2)- Tension

objective_function = lambda x : [cable_compatability(x), rod_compatability(x), force_balance(x)]


root = fsolve(objective_function, [1, 1, 1])
assert np.isclose(objective_function(root), [0.0, 0.0, 0.0]).all()  # func(root) should be almost 0.0.
print ("****************** Crossing Cables *******************")
print ("Cable Force: {} N".format(round(root[0]*1000, 2)))
print ("Rod Force/Stress: {} N, {} MPa".format(round(root[1]*1000, 2), round(root[1]/rod_area/1000, 2)))
print ("Deflection: {} mm, {} deg".format(round(root[2]*1000, 2),round( math.asin(get_sin_deflection_angle(root[2]))*180/pi, 2)))

print ("****************** Single Cable **********************")
lc = l
h = 0
cable_diameter = 1.0/8*25.4/1000 # m 
rod_od =  0.5 * 25.4/1000 # m 
rod_id = 0.43 * 25.4/1000 # m
rod_area = pi*(rod_od**2- rod_id**2)/4
cable_area = pi*cable_diameter**2/4

force_balance = lambda x : x[1] * get_sin_deflection_angle(x[2]) + x[0]*(h+x[2])/math.sqrt(l**2 + (h+x[2])**2)- Tension
objective_function = lambda x : [cable_compatability(x), rod_compatability(x), force_balance(x)]
root = fsolve(objective_function, [1, 1, 1])

assert np.isclose(objective_function(root), [0.0, 0.0, 0.0]).all()  # func(root) should be almost 0.0.



print ("Cable Force: {} N".format(round(root[0]*1000, 2)))
print ("Rod Force/Stress: {} N, {} MPa".format(round(root[1]*1000, 2), round(root[1]/rod_area/1000, 2)))
print ("Deflection: {} mm, {} deg".format(round(root[2]*1000, 2),round( math.asin(get_sin_deflection_angle(root[2]))*180/pi, 2)))

print ("****************** No Cable **************************")
rod_od =  9.525/1000 #0.5 * 25.4/1000 # m 
rod_id =0 #0.43 * 25.4/1000 # m
rod_area = pi*(rod_od**2- rod_id**2)/4
force_balance = lambda x : x[0] * get_sin_deflection_angle(x[1]) - Tension
rod_compatability = lambda x: x[0] - get_Frod(x[1])
objective_function = lambda x : [rod_compatability(x), force_balance(x)]
root = fsolve(objective_function, [ 200, 0.01])

assert np.isclose(objective_function(root), [0.0, 0.0]).all() 

print ("Rod Force/Stress: {} N, {} MPa".format(round(root[0]*1000, 2), round(root[0]/rod_area/1000, 2)))
print ("Deflection: {} mm, {} deg".format(round(root[1]*1000, 2),round( math.asin(get_sin_deflection_angle(root[1]))*180/pi, 2)))