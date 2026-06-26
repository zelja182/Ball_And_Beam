function plot_resid_each_experiment(data, sys, fig_prefix, save_figures, out_dir)
    if nargin < 4
        save_figures = false;
    end
    if nargin < 5
        out_dir = '';
    end

    for k = 1:data.Ne
        exp_data = getexp(data, k);
        fig_name = sprintf('%s - Exp %d', fig_prefix, k);
        fig_handle = figure('Name', fig_name, 'NumberTitle', 'off');
        resid(sys, exp_data);

        if save_figures && ~isempty(out_dir)
            prefix = lower(strrep(fig_prefix, ' ', '_'));
            base_name = sprintf('%s_exp%02d', prefix, k);
            save_thesis_figure(fig_handle, base_name, out_dir);
        end
    end
end
