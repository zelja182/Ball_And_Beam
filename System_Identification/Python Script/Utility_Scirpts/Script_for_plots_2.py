import matplotlib.pyplot as plt
import pandas as pd


path_1 = "../Ball_And_Beam/System_Identification/Data/Encoder_data/Validation_data/Dir_2/"


# Create a figure and 3 subplots
fig, (ax0, ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8) = plt.subplots(9, 1, figsize=(6, 8))

fig.suptitle('Експеримент 3')
# Plot 0
output_data_path = path_1 + "Val_Data_0.csv"
df_0= pd.read_csv(output_data_path)
ax0.plot(df_0["Time_s"], df_0['Angles'], df_0['Time_s'], df_0['PWM'])

# Plot 1
output_data_path = path_1 + "Val_Data_1.csv"
df_0= pd.read_csv(output_data_path)
ax1.plot(df_0["Time_s"], df_0['Angles'], df_0['Time_s'], df_0['PWM'])

# Plot 2
output_data_path = path_1 + "Val_Data_2.csv"
df_0= pd.read_csv(output_data_path)
ax2.plot(df_0["Time_s"], df_0['Angles'], df_0['Time_s'], df_0['PWM'])

# Plot 3
output_data_path = path_1 + "Val_Data_3.csv"
df_0= pd.read_csv(output_data_path)
ax3.plot(df_0["Time_s"], df_0['Angles'], df_0['Time_s'], df_0['PWM'])

# Plot 4
output_data_path = path_1 + "Val_Data_4.csv"
df_0= pd.read_csv(output_data_path)
ax4.plot(df_0["Time_s"], df_0['Angles'], df_0['Time_s'], df_0['PWM'])

# Plot 5
output_data_path = path_1 + "Val_Data_5.csv"
df_0= pd.read_csv(output_data_path)
ax5.plot(df_0["Time_s"], df_0['Angles'], df_0['Time_s'], df_0['PWM'])

# Plot 6
output_data_path = path_1 + "Val_Data_6.csv"
df_0= pd.read_csv(output_data_path)
ax6.plot(df_0["Time_s"], df_0['Angles'], df_0['Time_s'], df_0['PWM'])

# Plot 7
output_data_path = path_1 + "Val_Data_7.csv"
df_0= pd.read_csv(output_data_path)
ax7.plot(df_0["Time_s"], df_0['Angles'], df_0['Time_s'], df_0['PWM'])

# Plot 8
output_data_path = path_1 + "Val_Data_8.csv"
df_0= pd.read_csv(output_data_path)
ax8.plot(df_0["Time_s"], df_0['Angles'], df_0['Time_s'], df_0['PWM'])

# Adjust layout to prevent overlap
plt.tight_layout()

# Show the plot
plt.show()
