import numpy as np
from scipy.optimize import minimize
from scipy.integrate import odeint
from scipy import signal
import pandas as pd
import matplotlib.pyplot as plt


'''Show plot and validation functions'''

def show_plot(sim_time, sim_out, input_t, input_out, input_pwm):
    plt.plot(sim_time, sim_out, input_t, input_out, input_t, input_pwm)
    plt.grid()
    # plt.title("Test " + str(idx))
    plt.xlabel("Time [s]")
    plt.ylabel("Angle")
    plt.show()

def validate(a, b):
    sys = signal.StateSpace(-a, b, 1, 0)    
    mse = np.empty(shape=(2,10))
    for idx_1 in range(1,3):
        for idx_2 in range(10): 
            try:
                val_path = "../Ball_And_Beam/System_Identification/Data/Encoder_data/Validation_data/Dir_"+str(idx_1)+"/Val_Data_"+str(idx_2)+".csv"
                val_data = pd.read_csv(val_path)
                val_in = val_data["PWM"].to_numpy()
                val_t = val_data["Time_s"].to_numpy()
                val_out = val_data["Angles"].to_numpy()

                tout, yout, _ = signal.lsim(system=sys, U=val_in, T=val_t)  # simulate
                mse[idx_1-1][idx_2] = np.mean((val_out - yout)**2)  # calculate mean squere error
                # show_plot(sim_time=tout, sim_out=yout, input_t=val_t, input_pwm=val_in, input_out=val_out)
            except FileNotFoundError:
                mse[idx_1-1][idx_2] = None
            except Exception as e:
                print('Test {}-{}'.format(idx_1, idx_2))
                print(e)

    return mse
    # return np.average(mse)
    


'''System Identification functions'''
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
    path_1 = "../Ball_And_Beam/System_Identification/Data/Encoder_data/Test_"
    est_path = "../Ball_And_Beam/System_Identification/Data/Estimation_data/Grey_Box.csv"

    est_data = {
        'test': [], 'a': [], 'b': [], 'mse-0-0' : [], 'mse-0-1' : [], 'mse-0-2' : [], 'mse-0-3' : [], 
        'mse-0-4' : [], 'mse-0-5' : [], 'mse-0-6' : [], 'mse-0-7' : [], 'mse-0-8' : [], 'mse-0-9' : [], 
        'mse-1-0' : [], 'mse-1-1' : [], 'mse-1-2' : [], 'mse-1-3' : [], 'mse-1-4' : [], 'mse-1-5' : [], 
        'mse-1-6' : [], 'mse-1-7' : [], 'mse-1-8' : [], 'mse-1-9' : [], 'mse-0-0' : [], 'mse-0-1' : [], 
        'mse-0-2' : [], 'mse-0-3' : [], 'mse-0-4' : [], 'mse-0-5' : [], 'mse-0-6' : [], 'mse-0-7' : [], 
        'mse-0-8' : [], 'mse-0-9' : [], 'mse-1-0' : [], 'mse-1-1' : [], 'mse-1-2' : [], 'mse-1-3' : [], 
        'mse-1-4' : [], 'mse-1-5' : [], 'mse-1-6' : [], 'mse-1-7' : [], 'mse-1-8' : [], 'mse-1-9' : []          
        }
    
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
                msError = validate(a=a0, b=b)

                est_data['test'].append(str(i)+"-"+str(j))
                est_data['a'].append(a0)
                est_data['b'].append(b)
                for idx_1 in range(2):
                    for idx_2 in range(10):
                        try:
                            est_data["mse-"+str(idx_1)+"-"+str(idx_2)].append(msError[idx_1][idx_2])
                        except Exception as ex:
                            print(ex)

            except FileNotFoundError:
                i = i+1
            except Exception as e:
                print(e)
    
    # print(est_data)
    out_data = pd.DataFrame(est_data)
    # out_data["a"].
    out_data.to_csv(est_path)



