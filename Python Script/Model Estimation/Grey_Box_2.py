import numpy as np
from scipy.optimize import minimize
from scipy.integrate import odeint
import pandas as pd

# Define the state-space model
def state_space_model(X, t, u, a0, b):
    A = -a0
    B = b
    return (A * X) + (B * u(t)).flatten()


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
        X = odeint(state_space_model, X0, [t[ti], t[ti+1]], args=(u, a0, b))[-1]
        y_model.append(compute_output(X))
        X0 = X  # Update initial condition for the next step

    y_model = np.array(y_model)
    return np.sum((y[1:] - y_model)**2)  # Sum of squared errors

# Example usage
# Assuming t, u, y are your time, input, and output data arrays respectively

# Define the input function
def u(t):
    # Here you should define how the input varies with time
    # This is a placeholder example
    return np.interp(t, t_array, u_array)

path_1 = "D:/Projekti/Za master rad/Servo_motor_model_identification/Data/Encoder_data/Test_1/Processed_2/"

output_data_path = path_1 + "Test_3.csv"
df = pd.read_csv(output_data_path)
df = df.drop(df[df["Time_s"]>=2.00].index)
y_array= df["Angles"].to_numpy()
print(len(y_array))
u_array = np.ones(len(y_array))*30
t_array = np.linspace(0, 2, 200)

# Initial guess for parameters
initial_guess = [1, 1]

# Perform the optimization
result = minimize(objective, initial_guess, args=(t_array, u, y_array))

# Extract the identified parameters
a0, b = result.x
print(f'Identified parameters: a0={a0},  b={b}')




