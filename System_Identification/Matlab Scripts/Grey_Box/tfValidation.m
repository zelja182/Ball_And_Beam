close all
clear all
clc
 
% Generate transferfunction
num = [0.509897713282462, 228.82356592561126];
den = [1, 24.31577422764982, 256.4989025643107];
sys = tf(num, den);

dir_path = "..\Ball_And_Beam\System_Identification\Data\Encoder_data\Validation_data\Dir_";

for i = 1:2
    for j = 0:8
        try
            final_path = dir_path + int2str(i) + '\Val_Data_' + int2str(j) + '.csv';

            T = readtable(final_path, 'ReadVariableNames', true);
            data = iddata(T.Angles, T.PWM, 0.01);
            
            fig_no = i*10+j;
            figure(fig_no);
            compare(data, sys);
      
            fig_no_2 = 100+i*10+j;
            figure(fig_no_2);
            resid(sys, data);            
            
         catch ME
            if (strcmp(ME.identifier, 'MATLAB:readtable:OpenFailed'))
                ;
            else
                disp(ME)
            end
        end
    end
end
