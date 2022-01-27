syms s t d1 d2 d3

H = s^3*d1+s^2*d2+s*d3;
H_inv = 1/H;
Hinv_pf = partfrac(H_inv,s)
Hinv_t = ilaplace(H_inv)
(exp(-(d2*t)/(2*d1))*(cosh((t*(d2^2/4 - d1*d3)^(1/2))/d1) + (d2*sinh((t*(d2^2/4 - d1*d3)^(1/2))/d1))/(2*(d2^2/4 - d1*d3)^(1/2))))/d3
 