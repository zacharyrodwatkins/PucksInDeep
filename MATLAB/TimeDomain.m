DiffDriveGantry;
H_theta_inv = inv(H);
H_theta_inv_t = ilaplace(H_theta_inv);
H_t = ilaplace(H);


f1 = matlabFunction(H_t(1,1));
f2 = matlabFunction(H_t(1,2));
f3 = matlabFunction(H_t(2,1));
f4 = matlabFunction(H_t(2,2));

h1 = f1(t_numerical);
h2 = f4(t_numerical);

vpa(f1)
vpa(f4)
vpa(f3)

% hold on
% for f = [f1,f2,f3,f4]
%     func = matlabFunction(f);
%     plot(t_numerical, func(t_numerical))
% end

% 
% plot(t_numerical, h2);
% 
% a = 44;      % m/s2
% v_max = 6;   % m/s
% X_t = [0;heaviside(t)*(a*t^2)/2-(2*a*(t-v_max/a)^2)/2*heaviside(t-v_max/a)];
% Y_func = matlabFunction(X_t(2));
% Y = Y_func(t_for_Y);
% 
% V = zeros(length(H),1);
% 
% for j  = 1:length(t_for_Y)
%     val = 0;
%     for i = 1:j
%         val = val + Y(i)*h2(j)*delta_t;
%     end
%     V(j) = val;
% end
% plot(t_for_Y,V)


% V = zeros(1,length(t_for_Y))