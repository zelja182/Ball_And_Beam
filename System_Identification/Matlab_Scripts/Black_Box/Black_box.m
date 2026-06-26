close all
clear all
clc

Ts = 0.01;
SAVE_FIGURES = true;
FIG_OUT_DIR = fullfile(fileparts(mfilename('fullpath')), 'figures');

training_data = load_iddata_from_list('train_list.txt', Ts);
validation_data = load_iddata_from_list('validation_list.txt', Ts);

fprintf('Training experiments: %d\n', training_data.Ne);
fprintf('Validation experiments: %d\n', validation_data.Ne);

net = cascadeforwardnet([2, 3, 4, 3, 2]);
N2 = neuralnet(net);
sys = nlarx(training_data, [4 4 0], N2);
disp('Estimation is done');

if SAVE_FIGURES
    save_base_train = 'training_compare';
    save_base_val = 'validation_compare';
else
    save_base_train = '';
    save_base_val = '';
end

plot_compare_subplots(training_data, sys, 'Training - model comparison', ...
    'training', save_base_train, FIG_OUT_DIR);
plot_resid_each_experiment(training_data, sys, 'Training - residuals', ...
    SAVE_FIGURES, fullfile(FIG_OUT_DIR, 'training_residuals'));

plot_compare_subplots(validation_data, sys, 'Validation - model comparison', ...
    'validation', save_base_val, FIG_OUT_DIR);
plot_resid_each_experiment(validation_data, sys, 'Validation - residuals', ...
    SAVE_FIGURES, fullfile(FIG_OUT_DIR, 'validation_residuals'));

if SAVE_FIGURES
    fprintf('Thesis figures saved under: %s\n', FIG_OUT_DIR);
end
