syms s t L R J_L J_S b1 b2 K

H_theta = ((L*s+R)/K)*[s^2*J_L+s*b1+(K^2*s)/(L*s+R) s^2*J_S; s^2*J_S s^2*J_L+s*b2+(K^2*s)/(L*s+R)];
H_time_domain = ilaplace(inv(H_theta))