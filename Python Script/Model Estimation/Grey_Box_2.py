import numpy as np
from scipy.optimize import minimize
from scipy.integrate import odeint
from scipy import signal
import pandas as pd
import matplotlib.pyplot as plt


def show_plot(sim_time, sim_out, input_t, input_out, input_pwm):
    plt.plot(sim_time, sim_out, input_t, input_out, input_t, input_pwm)
    plt.grid()
    # plt.title("Test " + str(idx))
    plt.xlabel("Time [s]")
    plt.ylabel("Angle")
    plt.show()

# Define the state-space model
def state_space_model(X, t, u, a0, b):
    A = -a0
    B = b
    return (A * X) + (B * u).flatten()


# Define the function to compute the output y
def compute_output(X):
    C = np.array([1, 0, 0])
    return C @ X

# Objective function to minimize
def objective(params, t, u, y):
    a0, b = params
    X0 = np.zeros(3)  # Assuming initial state is zero; adjust if needed
    y_model = []

    for ti in range(len(t) - 1):
        X = odeint(state_space_model, X0, [t[ti], t[ti+1]], args=(u[ti], a0, b))[-1]
        y_model.append(compute_output(X))
        X0 = X  # Update initial condition for the next step

    y_model = np.array(y_model)
    return np.sum((y[1:] - y_model)**2)  # Sum of squared errors

def estimate_params(time_array, input_array, output_array):
    initial_guess = [1, 1]
    return minimize(objective, initial_guess, args=(time_array, input_array, output_array), method='BFGS').x

if __name__ == "__main__":
    # paths to data 
    path_1 = "../Servo_motor_model_identification/Data/Encoder_data/Test_"
    val_path_1 = "../Servo_motor_model_identification/Data/Encoder_data/Validation_data/Validation_data_1.csv"
    val_path_2 = "../Servo_motor_model_identification/Data/Encoder_data/Validation_data/Validation_data_2.csv"
    est_path = "../Servo_motor_model_identification/Data/Estimation_data/Grey_Box.csv"

    est_data = {'a': [], 'b': [], 'mse_1': [], 'mse_2': []}

    val_data_1 = pd.read_csv(val_path_1)
    val_in_1 = val_data_1["PWM"].to_numpy()
    val_t_1 = val_data_1["Time_s"].to_numpy()
    val_out_1 = val_data_1["Angles"].to_numpy()

    val_data_2 = pd.read_csv(val_path_2)
    val_in_2 = val_data_2["PWM"].to_numpy()
    val_t_2 = val_data_2["Time_s"].to_numpy()
    val_out_2 = val_data_2["Angles"].to_numpy()

    
    for i in range(1,3):
        dir_path = path_1 + str(i)
        for j in range(30):
            try:
                file_path = dir_path + "/Processed/Test_" + str(j) + ".csv"
                # generate input
                df = pd.read_csv(file_path)
                df = df.drop(df[df["Time_s"]>=2.00].index)
                y_array= df["Angles"].to_numpy()
                y_array[0] = 0
                u_array = df["PWM"].to_numpy()
                t_array = df["Time_s"].to_numpy()

                # # estimate values of state space system
                a0, b = estimate_params(time_array=t_array, input_array=u_array, output_array=y_array)

                # simulation and validation 
                sys = signal.StateSpace(-a0, b, 1, 0)

                tout, yout, xout = signal.lsim(system=sys, U=val_in_1, T=val_t_1)
                mse_1 = np.mean((val_out_1 - yout)**2)
                show_plot(sim_time=tout, sim_out=yout, input_t=val_t_1, input_pwm=val_in_1, input_out=val_out_1)

                tout, yout, xout = signal.lsim(system=sys, U=val_in_2, T=val_t_2)
                mse_2 = np.mean((val_out_2 - yout)**2)
                show_plot(sim_time=tout, sim_out=yout, input_t=val_t_2, input_pwm=val_in_2, input_out=val_out_2)

                est_data["a"].append(a0)
                est_data["b"].append(b)
                est_data["mse_1"].append(mse_1)
                est_data["mse_2"].append(mse_2)
                # print(f'Identified parameters: a0={a0},  b={b}, mse_1={mse_1}, mse_2={mse_2}')

            except FileNotFoundError:
                i = i+1
            except Exception as e:
                print(e)
    
    out_data = pd.DataFrame(est_data)
    out_data.to_csv(est_path)



