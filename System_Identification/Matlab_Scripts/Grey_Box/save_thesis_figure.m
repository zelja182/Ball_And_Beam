function save_thesis_figure(fig_handle, base_name, out_dir)
    if ~exist(out_dir, 'dir')
        mkdir(out_dir);
    end

    png_path = fullfile(out_dir, [base_name, '.png']);
    pdf_path = fullfile(out_dir, [base_name, '.pdf']);

    print(fig_handle, png_path, '-dpng', '-r300');
    print(fig_handle, pdf_path, '-dpdf', '-bestfit');

    fprintf('Saved: %s\n', png_path);
end
