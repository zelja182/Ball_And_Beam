function plot_models_compare_all(candidates, validation_dirs, set_names, fig_root, test_indices)
    if nargin < 5 || isempty(test_indices)
        test_indices = 0:14;
    end

    model_colors = [
        0.85, 0.33, 0.10
        0.00, 0.45, 0.74
        0.47, 0.67, 0.19
    ];

    dataset_order = [2, 1];  % Test_30, then Test_45

    compare_dir = fullfile(fig_root, 'compare');
    if ~exist(compare_dir, 'dir')
        mkdir(compare_dir);
    end

    sys_list = cell(1, numel(candidates));
    for c = 1:numel(candidates)
        sys_list{c} = tf(candidates(c).num, candidates(c).den);
    end

    legend_entries = [{'Measured'}, {candidates.name}];

    for j = test_indices
        fig = figure('Visible', 'off', 'NumberTitle', 'off', ...
            'Units', 'centimeters', 'Position', [1, 1, 42, 16]);
        has_data = false;

        for panel = 1:numel(dataset_order)
            s = dataset_order(panel);
            final_path = fullfile(validation_dirs{s}, sprintf('Test_%d.csv', j));
            if ~exist(final_path, 'file')
                continue;
            end

            T = readtable(final_path, 'ReadVariableNames', true);
            has_data = true;

            subplot(1, 2, panel);
            plot(T.Time_s, T.Angles, 'b', 'LineWidth', 1.2);
            hold on;

            for c = 1:numel(candidates)
                y = lsim(sys_list{c}, T.PWM, T.Time_s);
                plot(T.Time_s, y, '--', 'Color', model_colors(c, :), 'LineWidth', 1.1);
            end
            hold off;

            grid on;
            title(set_names{s}, 'FontWeight', 'normal');
            xlabel('Time (s)');
            ylabel('Angle (deg)');

            if panel == 1
                legend(legend_entries, 'Location', 'best');
            end
        end

        if ~has_data
            close(fig);
            continue;
        end

        add_figure_title(sprintf('Validation Test_%d - model comparison', j));
        save_thesis_figure(fig, sprintf('Test_%d_model_compare', j), compare_dir);
        close(fig);
    end
end
