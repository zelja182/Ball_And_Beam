function data = load_iddata_from_list(list_path, Ts)
    script_dir = fileparts(mfilename('fullpath'));
    list_file = fullfile(script_dir, list_path);
    paths = read_list_lines(list_file);

    n = numel(paths);
    Y = cell(1, n);
    U = cell(1, n);

    for k = 1:n
        T = readtable(fullfile(script_dir, paths{k}));
        Y{k} = T.Angles;
        U{k} = T.PWM;
    end

    data = iddata(Y, U, Ts);
end

function lines = read_list_lines(list_file)
    fid = fopen(list_file, 'r');
    if fid == -1
        error('Cannot open file: %s', list_file);
    end

    lines = {};
    tline = fgetl(fid);
    while ischar(tline)
        tline = strtrim(tline);
        if ~isempty(tline) && tline(1) ~= '#'
            lines{end + 1} = tline; %#ok<AGROW>
        end
        tline = fgetl(fid);
    end

    fclose(fid);
end
