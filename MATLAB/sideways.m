syms s t x p1  p2 p3;

DiffDriveGantry;
V_nom = 12.5*50/128;
Hss = p1*s^3+p2*s^2+p3*s;
invHt = ilaplace(inv(Hss),t);
invHt_func = matlabFunction(invHt);
theta_symb = int(V_nom*invHt,t,0,x);


p1_start = L/K*(J_L+J_S);
p2_start = (R*(J_L+J_S)+L*(bl+bs))/K;
p3_start = K + R*(b1+bs)/K;

theta_func = matlabFunction(theta_symb);
Table = readtable('26-01-3\run-1.txt','NumHeaderLines',10);
x = table2array(Table(:,6))/1000;
x = x - x(1);
theta_exp = table2array(Table(:,1))*pi/180;
theta_exp = theta_exp - theta_exp(1);
[fitted_curve,gof] = fit(x,theta_exp,theta_func,'StartPoint', ...
    [p1_start,p2_start,p3_start])
p = coeffvalues(fitted_curve);
theta_pred = theta_func(p(1),p(2),p(3),x);
hold on
plot(x,theta_pred);
plot(x,theta_exp);
legend("Predicted","Experimental","Location", "best")
hold off
