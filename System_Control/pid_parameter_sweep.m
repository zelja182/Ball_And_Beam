% Sweep Kp, Ki or Kd in PID_systems.slx and save responses to CSV.
% Plot later with plot_pid_sweep.py.
%
% Set r_0 to the initial ball position [mm]. In the model, set the ball
% position Integrator Initial condition to the workspace variable r_0.
%
% Model layout (same file):
%   top    = nonlinear ball + grey-box servo TF
%   bottom = nonlinear ball + black-box (Nonlinear ARX) servo
%   Both loops share workspace gains Kp, Ki, Kd and initial position r_0.
%   To Workspace (timeseries, Mux = [servo_angle; ball_position]):
%   grey_box_data, black_box_data

close all
clc

model = 'PID_systems';
grey_var = 'grey_box_data';
black_var = 'black_box_data';

sweep_param = 'r_0';          % only this gain is iterated
sweep_values = [380, 379, 71, 70];

Kp = -1.2;                     % held constant
Ki = -0.01;                      % held constant
Kd = -0.7;                      % overwritten each loop by sweep_values
r_0 = 378;                     % initial ball position [mm]; set Integrator IC to r_0 in the model
stop_time = 15;

this_dir = fileparts(mfilename('fullpath'));
data_dir = fullfile(this_dir, 'Data');
if ~exist(data_dir, 'dir')
    mkdir(data_dir);
end

% Nonlinear ARX block reads workspace variable "sys".
bb_mat = fullfile(this_dir, 'black_box_model.mat');
if exist(bb_mat, 'file')
    loaded = load(bb_mat);
    if isfield(loaded, 'sys')
        assignin('base', 'sys', loaded.sys);
    else
        warning(['black_box_model.mat has no variable "sys". ', ...
            'Ensure sys is in the base workspace before sim.']);
    end
elseif evalin('base', 'exist(''sys'', ''var'')') == 0
    warning(['sys not found. Load the Nonlinear ARX model into ', ...
        'base workspace as "sys" before running this script.']);
end

load_system(model);
set_param(model, 'StopTime', num2str(stop_time));
% Dead zone + pure Derivative can chatter against servo saturation (±45°),
% which trips consecutive zero-crossing limits and stops the sim.
set_param(model, 'ZeroCrossAlgorithm', 'Adaptive');
set_param(model, 'MaxConsecutiveZCsMsg', 'none');
zc_blocks = [ ...
    find_system(model, 'SearchDepth', 1, 'BlockType', 'Saturate'); ...
    find_system(model, 'SearchDepth', 1, 'BlockType', 'DeadZone')];
for i = 1:numel(zc_blocks)
    set_param(zc_blocks{i}, 'ZeroCross', 'off');
end

all_rows = table();

for k = 1:numel(sweep_values)
    assignin('base', 'Kp', Kp);
    assignin('base', 'Ki', Ki);
    assignin('base', 'Kd', Kd);
    assignin('base', 'r_0', r_0);
    assignin('base', sweep_param, sweep_values(k));

    sim(model);

    grey = evalin('base', grey_var);
    black = evalin('base', black_var);

    [t, servo_grey, ball_grey] = unpack_mux_ts(grey);
    [~, servo_black, ball_black] = unpack_mux_ts(black);

    Kp_run = Kp;
    Ki_run = Ki;
    Kd_run = Kd;
    r0_run = r_0;
    switch sweep_param
        case 'Kp'
            Kp_run = sweep_values(k);
        case 'Ki'
            Ki_run = sweep_values(k);
        case 'Kd'
            Kd_run = sweep_values(k);
        case 'r_0'
            r0_run = sweep_values(k);
    end

    n_samples = numel(t);
    run_rows = table( ...
        t, ball_grey, servo_grey, ball_black, servo_black, ...
        repmat(Kp_run, n_samples, 1), ...
        repmat(Ki_run, n_samples, 1), ...
        repmat(Kd_run, n_samples, 1), ...
        repmat(r0_run, n_samples, 1), ...
        'VariableNames', { ...
            'time_s', 'ball_grey', 'servo_grey', ...
            'ball_black', 'servo_black', 'Kp', 'Ki', 'Kd', 'r_0'});
    all_rows = [all_rows; run_rows]; %#ok<AGROW>
end

csv_path = fullfile(data_dir, sprintf('pid_sweep_%s.csv', sweep_param));
writetable(all_rows, csv_path);
fprintf('Saved %s\n', csv_path);

function [t, servo, ball] = unpack_mux_ts(ts_in)
% Mux order in PID_systems.slx: [control/servo angle; ball position]
    if isa(ts_in, 'timeseries')
        t = ts_in.Time(:);
        data = squeeze(ts_in.Data);
    elseif isstruct(ts_in) && isfield(ts_in, 'time') && isfield(ts_in, 'signals')
        t = ts_in.time(:);
        data = squeeze(ts_in.signals.values);
    else
        error('Unexpected To Workspace format: %s', class(ts_in));
    end

    if isvector(data)
        error(['Mux data has only one channel. Expected 2: ' ...
            'servo angle and ball position.']);
    end

    if size(data, 1) ~= numel(t) && size(data, 2) == numel(t)
        data = data.';
    end

    servo = data(:, 1);
    ball = data(:, 2);
end
