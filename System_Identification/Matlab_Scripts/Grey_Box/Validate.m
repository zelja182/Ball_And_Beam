function [MSE] = Validate(num,den)
%VALIDATE Summary of this function goes here
%   Detailed explanation goes here
    
    dir_path = "..\Ball_And_Beam\System_Identification\Data\Encoder_data\Test_2\Test_45\Processed\Test_";
    
    errorData= struct();
    sys = tf(num, den);
    

    for j = 0:15
        try
            final_path = dir_path + int2str(j) + '.csv';
            T = readtable(final_path, 'ReadVariableNames', true);
            [y, ] = lsim(sys, T.PWM, T.Time_s);
            test_no = sprintf('mse_%d', j);
            errorData.(test_no) = immse(T.Angles, y);

         catch ME
            if (strcmp(ME.identifier, 'MATLAB:readtable:OpenFailed'))
                ;
            else
                disp(ME)
            end
        end
    end

    
    MSE = errorData;   
    
end

