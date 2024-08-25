import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal as si


def show_plot(time_s, angle, pwm, idx):
    plt.figure(idx)
    plt.plot(time_s, angle, time_s, pwm)
    plt.grid()
    plt.title("Test " + str(idx))
    plt.xlabel("Time [s]")
    plt.ylabel("Angle")
    plt.show()


path_1 = "../Ball_And_Beam/System_Identification/Data/Encoder_data/Test_2/Processed/"
relativ_error = np.zeros((4, 5))
relativ_error_1 = np.zeros((6, 5))
exp_value = [30, 45, 60, 90]
exp_value_1 = [-60, -45, -30, 30, 45, 60]

j = -1

'''
Odredjivanje Relativne greske
'''
for i in range(20):
    if not i%5:
        j = j + 1
    try:
        # Load data 
        output_data_path = path_1 + "Test_" + str(i)  + ".json"
        df = pd.read_json(output_data_path)

        # Convert data
        # df["Angles"] = df["Counts"]*360.0/600.0
        # df["Time_s"] = df["Time"]/1000000000
    
        # print(df)
        # # Data filtering 
        # df_2 = pd.DataFrame()     
        # df_2 = df.drop(range(df[df.Time_s > 2].index[0]+1, len(df.index)))  # remove values after t>2s
        # # print(df_2)
        # peaks = si.find_peaks(abs(df_2["Angles"]))  # find all peaks
        # # print(peaks)
        # df_2 = df_2.drop(range(0, peaks[0][-1], 1))  # remove all peaks 
        # df_2.reset_index(drop=True, inplace=True)  # reset index 
        # relativ_error[j][i%5]= (df_2["Angles"][0] - exp_value[j])/exp_value[j]  # Calculate relative error 
        show_plot(time_s=df["Time_s"], angle=df["Angles"], idx=i, pwm=df["PWM"])
    except:
        print("Data not found or relavant")
        relativ_error[j][i%5] = np.nan

print("Matrica relativnih gresaka:")
print(relativ_error)