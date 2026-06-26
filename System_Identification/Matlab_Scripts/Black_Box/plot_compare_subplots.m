function fig_handle = plot_compare_subplots(data, sys, fig_name, layout, save_base_name, out_dir)
    if nargin < 4 || isempty(layout)
        layout = 'auto';
    end
    if nargin < 5
        save_base_name = '';
    end
    if nargin < 6
        out_dir = '';
    end

    n = data.Ne;
    fig_handle = open_thesis_figure(fig_name, layout, n);
    style_thesis_axes();

    for k = 1:n
        ax_idx = thesis_subplot_index(k, layout, n);
        subplot(ax_idx(1), ax_idx(2), ax_idx(3));

        exp_data = getexp(data, k);
        y_sim = sim(sys, exp_data);
        t = get_iddata_time(exp_data);
        t_sim = get_iddata_time(y_sim);

        plot(t, exp_data.y(:, 1), 'b', 'LineWidth', 1.1);
        hold on;
        plot(t_sim, y_sim.y(:, 1), 'r--', 'LineWidth', 1.1);
        hold off;

        grid on;
        title(sprintf('Exp %d', k), 'FontWeight', 'normal');
        xlabel('Time (s)');
        ylabel('Angle (deg)');

        if k == 1
            legend('Measured', 'Model', 'Location', 'best');
        end
    end

    hide_unused_subplots(layout, n);
    add_figure_title(fig_name);

    if ~isempty(save_base_name) && ~isempty(out_dir)
        save_thesis_figure(fig_handle, save_base_name, out_dir);
    end
end

function fig_handle = open_thesis_figure(fig_name, layout, n)
    switch layout
        case 'training'
            fig_handle = figure( ...
                'Name', fig_name, ...
                'NumberTitle', 'off', ...
                'Units', 'centimeters', ...
                'Position', [1, 1, 42, 56]);
        case 'validation'
            fig_handle = figure( ...
                'Name', fig_name, ...
                'NumberTitle', 'off', ...
                'Units', 'centimeters', ...
                'Position', [1, 1, 42, 22]);
        otherwise
            ncols = ceil(sqrt(n));
            nrows = ceil(n / ncols);
            fig_handle = figure( ...
                'Name', fig_name, ...
                'NumberTitle', 'off', ...
                'Units', 'centimeters', ...
                'Position', [1, 1, 6 * ncols, 4.5 * nrows]);
    end
end

function idx = thesis_subplot_index(k, layout, n)
    switch layout
        case 'training'
            % 3 x 7 grid for first 21 runs, last run centered on row 8
            if k <= 21
                idx = [8, 3, k];
            else
                idx = [8, 3, 23];
            end
        case 'validation'
            % 2 x 4 grid (8 slots) for up to 7 validation runs
            idx = [2, 4, k];
        otherwise
            ncols = ceil(sqrt(n));
            idx = [ceil(n / ncols), ncols, k];
    end
end

function hide_unused_subplots(layout, n)
    if strcmp(layout, 'validation') && n < 8
        subplot(2, 4, 8);
        axis off;
    end
end

function add_figure_title(fig_name)
    % sgtitle requires R2018b+; use annotation on older MATLAB
    if exist('sgtitle', 'builtin') == 5
        sgtitle(fig_name, 'FontSize', 12, 'FontWeight', 'bold');
    else
        annotation('textbox', [0, 0.95, 1, 0.05], ...
            'String', fig_name, ...
            'EdgeColor', 'none', ...
            'HorizontalAlignment', 'center', ...
            'VerticalAlignment', 'top', ...
            'FontSize', 12, ...
            'FontWeight', 'bold');
    end
end

function style_thesis_axes()
    set(groot, 'DefaultAxesFontSize', 10);
    set(groot, 'DefaultLineLineWidth', 1.1);
end
