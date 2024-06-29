import numpy as np
import tensorflow as tf

# Example data: input_array and output_array
input_array = np.array([30, 30, 30, 30])  # Replace with your actual input data
output_array = np.array([0, 1, 2, 3])    # Replace with your actual output data

# Prepare the dataset for LSTM
X = []
y = []

initial_state = 0  # Initial state at t=0

for t in range(1, len(input_array)):
    X.append([input_array[t], output_array[t-1]])
    y.append(output_array[t])

X = np.array(X).reshape(-1, 1, 2)  # Reshape for LSTM input (samples, time steps, features)
y = np.array(y)

# Define the LSTM model
model = tf.keras.Sequential([
    tf.keras.layers.LSTM(64, input_shape=(1, 2), return_sequences=False),
    tf.keras.layers.Dense(1)
])

# Compile the model
model.compile(optimizer='adam', loss='mean_squared_error')

# Train the model
history = model.fit(X, y, epochs=100, validation_split=0.2, batch_size=1)

# Evaluate the model
mse = model.evaluate(X, y)
print(f'MSE: {mse}')

# Make predictions
predictions = model.predict(X)
print(predictions)
