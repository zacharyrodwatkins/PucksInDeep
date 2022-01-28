% Pulley Inertias and Geometry
R_LP = 0.07115/2;  % m
R_SP = 0.01;    % m
M_LP = 0.192; % kg
I_LP = 0.5*M_LP*R_LP^2;  % kg m2
I_SP = 8.26*10^(-6);  % kg m2

% Component Masses
M_belt = 0.08983;
M_SP = 0.003907;
M_bear_FB = 0.05395652;
M_mount_SP = 0.05;
M_guide_SS = 0.1162;
M_bear_SS = 0.0178;
M_mount_mal = 0.05;
M_mal = 0.17;

M_A = M_bear_SS + M_mount_mal + M_mal;   % kg
M_FB = 4*M_SP + 2*M_bear_FB + 2*M_mount_SP + M_guide_SS;    % kg
M_B3 = M_belt/3;      % mass of 2 belt lengths (~1/3 of the belt) (kg)

% Motor constants
I_M = (1.63*0.6*(0.079/2)^2)/2;   % kg m2
L = 0.00002;        % H
R = 0.666;          % ohm
Ke = 60/(2*3.14159*237);     % V/rad/s
Kt = Ke;      % Nm/A
K = Ke;         % Ke = Kt = K
b1 = 0.001;      % viscous friction term
b2 = 0.001;      % viscous friction term

bx = 5e-4;
by = 5e-4;

bl = b1+bx+by;
bs = bx-by;


% General Inertia Terms
% Torque needed for motor 1 is J_L*Omega1 + J_S*Omega2
J_L = (2*I_LP + I_M + (I_SP*R_LP^2)/(R_SP^2) + (M_A*R_LP^2)/2 + (M_FB*R_LP^2)/4 + R_LP^2*M_B3);
J_S = ((I_SP*R_LP^2)/(R_SP^2) - (M_FB*R_LP^2)/4);

% System Transfer Matrices
syms s t

H = (L*s+R)/(K*R_LP)*[s^2*(J_L+J_S)+s*(b1)+(s*K^2)/(L*s+R) s^2*(J_L-J_S)+s*(b1)+(s*K^2)/(L*s+R); s^2*(J_L+J_S)+s*(b2)+(s*K^2)/(L*s+R) s^2*(J_S-J_L)-s*(b2)-(s*K^2)/(L*s+R)];
H_vel = (L*s+R)/(K*R_LP)*[s*(J_L+J_S)+b1+K^2/(L*s+R) s*(J_L-J_S)+b1+K^2/(L*s+R); s*(J_L+J_S)+b2+K^2/(L*s+R) s*(J_S-J_L)-b2-K^2/(L*s+R)];
H_theta = ((L*s+R)/K)*[s^2*J_L+s*b1+(K^2*s)/(L*s+R) s^2*J_S; s^2*J_S s^2*J_L+s*b2+(K^2*s)/(L*s+R)];
H_theta_dot = ((L*s+R)/K)*[s*J_L+b1+(K^2)/(L*s+R) s*J_S; s*J_S s*J_L+b2+(K^2)/(L*s+R)];
H_I_vComp = inv([L*s+R 0; 0 L*s+R]);
H_I_omegaComp = -H_I_vComp*[K 0; 0 K];



% % V to x, x_dot, theta, omega conversion
% V_t = [24*heaviside(t);-24*heaviside(t)];
% V =laplace(V_t);
% X = inv(H)*V;
% Vel = inv(H_vel)*V;
% X_t = ilaplace(X);
% Vel_t = ilaplace(Vel);
% 
% omega = inv(H_theta_dot)*V
% %60/(2*3.1415)*
% omega_t = ilaplace(omega)
% I = H_I_vComp*V + H_I_omegaComp*omega;
% I_t = ilaplace(I);
% figure(1)
% hold on
% yyaxis left
% fplot(omega_t(1), [0, 3])
% fplot(omega_t(2), [0, 3])
% ylabel('Omega (rad/s)')
% yyaxis right
% fplot(I_t(1), [0, 3])
% fplot(I_t(2), [0, 3])
% ylabel('Current (A)')
% legend('Omega 1(t)', 'Omega 2(t)', 'Motor 1 Current', 'Motor 2 Current', 'Location','best')
% title('Angular Velocity vs Time')
% xlabel('Time (s)')
% hold off
% 
% figure(2)
% hold on
% fplot(X_t(1), [0, 2])
% fplot(X_t(2), [0, 2])
% legend('X(t)', 'Y(t)','Location','best')
% title('Position vs time')
% ylabel('Position(t) (m)')
% xlabel('time (s)')
% hold off
% figure(3)
% hold on
% fplot(Vel_t(1), [0, 2])
% fplot(Vel_t(2), [0, 2])
% legend('Vel_X(t)', 'Vel_Y(t)','Location','best')
% title('Velocity vs time')
% ylabel('Velocity(t) (m/s)')
% xlabel('time (s)')
% hold off

% % X to V and I conversion
% a = 44;      % m/s2
% v_max = 6;   % m/s
% X_t = [0;heaviside(t)*(a*t^2)/2-(2*a*(t-v_max/a)^2)/2*heaviside(t-v_max/a)];
% % X0 = heaviside(-t)*[0.5; 0.2];
% % X_t = X0 + (heaviside(t))*[(1.8*10^5*t^5 - 4.5*10^4*t^4 + 3*10^3*t^3 - 0.0*10^0*t^2 + 0.0*10^0*t + 5.0*10^(-1));1.50*10^5*t^5 - 4.05*10^4*t^4 + 3.10*10^3*t^3 - 0.00*10^0*t^2 + 0.00*10^0*t + 2.00*10^(-1)];
% % X_t = X0 + heaviside(t)*[493.82716049383083*t^5 + -370.3703703703728*t^4 + 74.0740740740745*t^3 + 0.5;-370.3703703703714*t^5 + 185.18518518518584*t^4 + -1.0279842820603364e-13*t^3 + 0.2];
% Vel_t = diff(X_t);
% X = laplace(X_t);
% V = H*X;
% omega = H_theta_dot\V;
% omega_t = ilaplace(omega);
% EMF_t = omega_t*Ke;
% V_t = ilaplace(V);
% I = H_I_vComp*V + H_I_omegaComp*omega;
% I_t = ilaplace(I);
% figure(3)
% hold on
% yyaxis left
% fplot(V_t(1), [0, 0.3])
% fplot(V_t(2), [0, 0.3])
% ylabel('Voltage (V)')
% yyaxis right
% fplot(I_t(1), [0, 0.3])
% fplot(I_t(2), [0, 0.3])
% ylabel('Current (A)')
% legend('Motor 1 Voltage', 'Motor 2 Voltage', 'Motor 1 Current','Motor 2 Current', 'Location','best')
% title('Voltage and Current vs time')
% xlabel('Time (s)')
% hold off
% 
% figure(4)
% hold on
% yyaxis left
% fplot(X_t(1), [0, 0.3])
% fplot(X_t(2), [0, 0.3])
% ylim([0,1])
% ylabel('Position (m)')
% xlabel('Time (s)')
% yyaxis right
% fplot(Vel_t(1), [0, 0.3])
% fplot(Vel_t(2), [0, 0.3])
% ylim([0,12])
% ylabel('Velocity (m/s)')
% legend('X', 'Y', 'Vx','Vy', 'Location','northwest')
% title('Position and Velocity vs time')
% hold off


% Logic Check against U Michigan Model
% figure(5)
% J = J_L;
% b = b1;
% P_motor = K/((J*s+b)*(L*s+R)+K^2);
% V = 10*heaviside(t);
% V_lap = laplace(V);
% t_dot_lap = V_lap*P_motor;
% t_dot = ilaplace(t_dot_lap);
% fplot(t_dot, [0,10])