close all
clear all
clc

sysData = struct();
dir_path = "..\Ball_And_Beam\System_Identification\Data\Encoder_data\Test_1\Processed\Test_";



% Polovi i nule
np = 2; % broj polova
nz = 0; % broj nula
file_path = "..\Ball_And_Beam\System_Identification\Data\Estimation_data\GreyBox\Model.json";

% Estimacija prenosne funkcije

for jdx = 0:40
    try
        final_path =  dir_path + int2str(jdx) + ".csv";
        T = readtable(final_path, 'ReadVariableNames', true);

        % Remove everything after t>= 2s and NaN values
        toDelete = T.PWM == 0.0;
        T(toDelete, :) = [];
        T = rmmissing(T);

        % Estimate tf and save num and den of sys
        data = iddata(T.Angles, T.PWM, 0.01);
        sys = tfest(data, np, nz);
        test_no = sprintf('test_%d', jdx);
        sysData.(test_no).num = sys.Numerator;
        sysData.(test_no).den = sys.Denominator;

        % Simulate and show on plot for quick validation 
        simTime = 0:0.01:length(T.PWM)/100-0.01;
        [y, tout] = lsim(sys, T.PWM, simTime);
        figure(jdx);
        plot(tout, y, T.Time_s, T.Angles);
        grid on; 

    catch ME
        if (strcmp(ME.identifier, 'MATLAB:readtable:OpenFailed'))
            ;
        else
            disp(ME)

        end
    end
end
% Validate data
keys = fieldnames(sysData);
for idx = 1:length(keys)
   curent_key = string(keys(idx));
   MSE_data = Validate(sysData.(curent_key).num, sysData.(curent_key).den); 
   sysData.(curent_key).MSE = MSE_data;
end

jsonData = jsonencode(sysData);

fileID = fopen(file_path, 'w');
if fileID == -1
    error('Cannot open file for writing: %s', file_path);
end
fprintf(fileID, '%s', jsonData);
fclose(fileID);

