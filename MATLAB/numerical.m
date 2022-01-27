deltas_coeffs = [- 1.2651567471463440739398720324971, - 0.1882019515052635039165096486613, -0.001966386005192808945213345239722];
% delat_coeffs;
a = 44;
y_func = @(t) 1/2*a*t^2;
y_dir = @(t) a*t;
y_acc = @(t) a;

Vfunc = @(t)  -1*deltas_coeffs(1)*y_dir(t) + deltas_coeffs(2)*y_acc(t);

t_num  = linspace(0,1);
plot(t_num, Vfunc(t_num));