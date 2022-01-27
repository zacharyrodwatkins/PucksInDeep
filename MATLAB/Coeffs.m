a1 = L*J_L/K;
a2 = (R*J_L+L*bl)/K;
a3 = (R*bl/K+K);
b1 = L*J_S;
b2 = (R*J_S+L*bs)/K;
b3 = R*bs/K;
a = [a1 a2 a3]
b= [b1 b2 b3]
d = a-b
p = a+b
d(3)
Topspeed_fb = 34/d(3)*R_LP
Topspeed_ss = 34/p(3)*R_LP
descrim = @(coeffs) coeffs(2)^2/4 - coeffs(1)*coeffs(3);
descrim(d)
descrim(p)
