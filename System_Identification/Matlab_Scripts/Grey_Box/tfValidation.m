close all
clear all
clc

% --- options ---
fit_pass = 80;
mse_pass = 15;
save_figures = true;
compare_test_indices = 0:14;  % use e.g. 4 for a single thesis figure (Test_4)

script_dir = fileparts(mfilename('fullpath'));
data_root = fullfile(script_dir, '..', '..', 'Data', 'Encoder_data');
fig_root = fullfile(script_dir, 'figures', 'grey_box_validation');
summary_path = fullfile(script_dir, '..', '..', 'Data', 'Estimation_data', ...
    'GreyBox', 'Validation_summary_candidates.csv');

% Three structurally different candidates (from Python ranking)
candidates = struct( ...
    'name', {'test_4', 'test_0', 'test_36'}, ...
    'num', {569.623354, 534.415036, 620.445479}, ...
    'den', { ...
        [1, 38.53635650251253, 593.7308494886121], ...
        [1, 37.084598037052665, 549.4238293240385], ...
        [1, 39.936997308422264, 637.821856677301] ...
    });

validation_dirs = {
    fullfile(data_root, 'Test_2', 'Test_45', 'Processed')
    fullfile(data_root, 'Test_2', 'Test_30', 'Processed')
};
set_names = {'Test_45', 'Test_30'};

if save_figures && ~exist(fig_root, 'dir')
    mkdir(fig_root);
end

fprintf('Data root: %s\n', data_root);
fprintf('Figure output: %s\n\n', fig_root);

model_col = strings(0);
dataset_col = strings(0);
test_col = strings(0);
case_col = strings(0);
fit_col = [];
mse_col = [];
pass_col = strings(0);

for c = 1:numel(candidates)
    model_name = candidates(c).name;
    sys = tf(candidates(c).num, candidates(c).den);
    resid_dir = fullfile(fig_root, 'residuals', model_name);

    fprintf('=== Validating %s ===\n', model_name);

    for s = 1:numel(validation_dirs)
        dir_path = validation_dirs{s};

        for j = 0:14
            final_path = fullfile(dir_path, sprintf('Test_%d.csv', j));
            try
                T = readtable(final_path, 'ReadVariableNames', true);
                data = iddata(T.Angles, T.PWM, 0.01);

                [~, fit] = compare(data, sys);
                y = lsim(sys, T.PWM, T.Time_s);
                mse = immse(T.Angles, y);

                if fit >= fit_pass && mse <= mse_pass
                    status = "PASS";
                else
                    status = "FAIL";
                end

                case_label = sprintf('%s_Test_%d', set_names{s}, j);

                model_col(end + 1, 1) = model_name;
                dataset_col(end + 1, 1) = set_names{s};
                test_col(end + 1, 1) = "Test_" + j;
                case_col(end + 1, 1) = case_label;
                fit_col(end + 1, 1) = fit;
                mse_col(end + 1, 1) = mse;
                pass_col(end + 1, 1) = status;

                if save_figures
                    fig = figure('Visible', 'off', 'Name', ...
                        sprintf('%s %s residual', model_name, case_label), ...
                        'NumberTitle', 'off');
                    resid(sys, data);
                    add_figure_title(sprintf('%s - %s - residuals', model_name, case_label));
                    save_thesis_figure(fig, ...
                        sprintf('%s_%s', model_name, case_label), resid_dir);
                    close(fig);
                end

            catch ME
                if strcmp(ME.identifier, 'MATLAB:readtable:OpenFailed')
                    fprintf('Skipping missing file: %s\n', final_path);
                else
                    disp(ME)
                end
            end
        end
    end
end

if isempty(fit_col)
    error('No validation files were loaded. Check data paths.');
end

summary = table(model_col, dataset_col, test_col, case_col, fit_col, mse_col, pass_col, ...
    'VariableNames', {'model', 'dataset', 'test', 'case_id', 'fit_pct', 'mse', 'status'});
writetable(summary, summary_path);

print_console_summary(summary, fit_pass, mse_pass);

if save_figures
    plot_models_compare_all(candidates, validation_dirs, set_names, fig_root, ...
        compare_test_indices);
    fprintf('\nFigures saved under:\n  %s\n', fullfile(fig_root, 'compare'));
end

fprintf('\nSummary saved to:\n  %s\n', summary_path);


function print_console_summary(summary, fit_pass, mse_pass)
    models = unique(summary.model);

    for i = 1:numel(models)
        block = summary(summary.model == models(i), :);
        block = sortrows(block, 'mse');
        n_pass = sum(block.status == "PASS");

        fprintf('\n=== %s ===\n', models(i));
        fprintf('Passed: %d / %d (fit >= %.0f%%, mse <= %.1f)\n', ...
            n_pass, height(block), fit_pass, mse_pass);
        fprintf('Mean MSE: %.2f   Median MSE: %.2f   Worst MSE: %.2f\n', ...
            mean(block.mse), median(block.mse), max(block.mse));
        fprintf('Best:  %s  fit=%.1f%%  mse=%.2f\n', ...
            block.case_id(1), block.fit_pct(1), block.mse(1));
        fprintf('Worst: %s  fit=%.1f%%  mse=%.2f\n', ...
            block.case_id(end), block.fit_pct(end), block.mse(end));
    end
end
