close all
clear all
clc

dir_path = "..\Ball_And_Beam\System_Identification\Data\Encoder_data\Test_2\Processed\Test_6.csv";
T = readtable(dir_path, 'ReadVariableNames', true);

% Remove everything afeter t>= 2s and NaN values
toDelete = T.Time_s >= 2.0;
T(toDelete, :) = [];
T = rmmissing(T);

% Generate data
data = iddata(T.Angles, T.PWM, 0.01);

% Generate transferfunction
num = 9.508274;
den = [1, 10.122469658724475];
sys = tf(num, den);

simTime = 0:0.01:length(T.PWM)/100-0.01;
[y, tout] = lsim(sys, T.PWM, simTime);
figure(1);
plot(tout, y, T.Time_s, T.Angles);
grid on; 

figure(2);
resid(sys, data);