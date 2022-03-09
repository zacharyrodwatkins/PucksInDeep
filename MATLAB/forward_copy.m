syms s t x d1  d2 d3;

DiffDriveGantry;
% V_t = 24.0*10/128*heaviside(t)-24.0*10/128*heaviside(t-1);  % step
V_t = 24.0*10/128*heaviside(t)-24.0*20/128*heaviside(t-1)+24.0*10/128*heaviside(t-2);  % double step
% V_t = 24*21/128*heaviside(t)*t - 24*21/128*t*heaviside(t-1);  % ramp
Hfb = d1*s^3+d2*s^2+d3*s;
invHt = ilaplace(inv(Hfb),t);
invHt_exp = 1/d3*(1-((exp(t*sqrt((d2/(2*d1))^2-d3/d1)-t*d2/(2*d1))+exp(-t*sqrt((d2/(2*d1))^2-d3/d1)-t*d2/(2*d1)))/2+(exp(t*sqrt((d2/(2*d1))^2-d3/d1)-t*d2/(2*d1))-exp(-t*sqrt((d2/(2*d1))^2-d3/d1)-t*d2/(2*d1)))/(2*sqrt((d2/(2*d1))^2-d3/d1))));
invHt_func = matlabFunction(invHt_exp);
theta_symb = int(V_t*invHt_exp,t,0,x);

d1_start = L/K*(J_L-J_S);
d2_start = (R*(J_L-J_S)+L*(bl-bs))/K;
d3_start = K + R*(bl-bs)/K;

theta_func = matlabFunction(theta_symb);
% Table = readtable('New_PS_ID/step_Speed_10.txt','NumHeaderLines',1);
Table = readtable('New_PS_ID/d_step_Speed_10.txt','NumHeaderLines',1);
% Table = readtable('New_PS_ID/ramp_uptoSpeed_21.txt','NumHeaderLines',1);
disp(Table)
t = table2array(Table(:,6));
t = t - t(1);
theta_exp = table2array(Table(:,1))*pi/180;
theta_exp = theta_exp - theta_exp(1);

invHt_func(d1_start,d2_start,d3_start,0.0440)

[fitted_curve,gof] = fit(t,theta_exp,theta_func,'StartPoint', ...
    [d1_start,d2_start,d3_start])
d = coeffvalues(fitted_curve);
theta_pred = theta_func(d(1),d(2),d(3),t);
hold on
plot(t,theta_pred);
plot(t,theta_exp);
legend("Predicted","Experimental","Location", "best")
hold off
