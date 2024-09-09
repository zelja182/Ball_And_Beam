function [MSE] = Validate(num,den)
%VALIDATE Summary of this function goes here
%   Detailed explanation goes here
    
    dir_path = "..\Ball_And_Beam\System_Identification\Data\Encoder_data\Validation_data\Dir_";
    errorData= struct();
    sys = tf(num, den);
    
    for i = 1:2
        for j = 0:8
            try
                final_path = dir_path + int2str(i) + '\Val_Data_' + int2str(j) + '.csv';
                T = readtable(final_path, 'ReadVariableNames', true);
                [y, ] = lsim(sys, T.PWM, T.Time_s);
                test_no = sprintf('mse_%d_%d', i, j);
                errorData.(test_no) = immse(T.Angles, y);
                
             catch ME
                if (strcmp(ME.identifier, 'MATLAB:readtable:OpenFailed'))
                    ;
                else
                    disp(ME)
                end
            end
        end
    end
    
    MSE = errorData;   
    
end

