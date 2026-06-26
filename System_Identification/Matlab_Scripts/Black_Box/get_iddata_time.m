function t = get_iddata_time(data)
    n = size(data.y, 1);
    t = data.Tstart + (0:n - 1)' * data.Ts;
end
