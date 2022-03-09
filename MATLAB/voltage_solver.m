syms t s

% d = [0.00354510685970849,0.0405895431472632,0.118802230207830];  %step
% p = [0.000715942393353209,0.0209125181612993,0.147120628806615];  %step

% d = [0.00541432557142285,0.00363316955384563,0.154349789580661];  %dstep
% p = [0.00149236152316467,0.00384918281227523,0.179747946423206];  %dstep

d = [0.0167490857864277,0.0377069291773955,0.185699248572345];  %ramp
p = [0.00327544946972679,-0.00123824009161343,0.154205588722957];  %ramp

% p = [0.0003, 0.0041, 0.1036];
% d =[0.0010, 0.0104, 0.0979];

a = (p+d)/2
b = (p-d)/2

R_LP = 0.07115/2;  % m
theta2xy = R_LP/2*[1,1; 1,-1] ;

% Solving for V(t) using ODE method
% acc = 10;
% v_max = 1;
% X = [-(heaviside(t)*(acc*t^2)/2-(2*acc*(t-v_max/acc)^2)/2*heaviside(t-v_max/acc));heaviside(t)*(acc*t^2)/2-(2*acc*(t-v_max/acc)^2)/2*heaviside(t-v_max/acc)];
% angle_vec = inv(theta2xy)*X;
% theta_t = angle_vec(1)
% phi_t = angle_vec(2)
theta_t = t^5-t^4-40*t^3+5*t^2-70*t;
theta_t_1 = diff(theta_t);
theta_t_2 = diff(theta_t,2);
theta_t_3 = diff(theta_t,3);
theta_vec = [theta_t_3; theta_t_2; theta_t_1];

phi_t = 0*t^5-10*t^4-80*t^3+t^2+65*t;
phi_t_1 = diff(phi_t);
phi_t_2 = diff(phi_t,2);
phi_t_3 = diff(phi_t,3);
phi_vec = [phi_t_3; phi_t_2; phi_t_1];

X = theta2xy*[theta_t;phi_t];

time = linspace(0,0.5,1000);
x_func = matlabFunction(X(1));
x = x_func(time);
y_func = matlabFunction(X(2));
y = y_func(time);

figure(5)
hold on
% fplot(X(1), [0, 1.3])
% fplot(X(2), [0, 1.3])
plot(x, y);
title('Path')
ylabel('Y pos (m)')
xlabel('X pos (m)')
hold off

V_t_ODE = [dot(a', theta_vec)+dot(b', phi_vec);dot(b', theta_vec)+dot(a', phi_vec)];
% 
% Coverting ODE solution back to motor angles to compare
% s_vec = [s^3, s^2, s];
% H_theta2volt = [dot(a, s_vec), dot(b, s_vec); dot(b, s_vec), dot(a, s_vec)];
% V_s_ODE = laplace(V_t_ODE);
% theta_check = ilaplace(inv(H_theta2volt)*V_s_ODE); 
% 
% figure(1)
% hold on
% fplot(theta_check(1), [0, 0.5]);
% fplot(theta_check(2), [0, 0.5]);
% legend('theta check(t)', 'phi check(t)', 'Location','best')
% title('motor angles vs time')
% ylabel('Angle (rad)')
% xlabel('time (s)')
% hold off
% 
% figure(2)
% hold on
% fplot(theta_t, [0, 0.5])
% fplot(phi_t, [0, 0.5])
% legend('theta(t)', 'phi(t)', 'Location','best')
% title('motor angles vs time')
% ylabel('Angle (rad)')
% xlabel('time (s)')
% hold off
% 
% figure(3)
% hold on
% fplot(X(1), [0, 0.5]);
% fplot(X(2), [0, 0.5]);
% legend('x(t)', 'y(t)', 'Location','best')
% title('mallet position vs time')
% ylabel('position (m)')
% xlabel('time (s)')
% hold off
% 
figure(2)
hold on
fplot(V_t_ODE(1), [0, 0.5])
fplot(V_t_ODE(2), [0, 0.5])
legend('V1(t)', 'V2(t)','Location','best')
title('Voltage vs time')
ylabel('Voltage(t) (V)')
xlabel('time (s)')
hold off