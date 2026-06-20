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


def get_brake_point(df):
    for i in range(len(df["Time_s"])):
        if df["Time_s"][i + 1] - df["Time_s"][i] > 0.03:
            return i + 1
    return False


# path_1 = "D:/Projekti/Ball_And_Beam/System_Identification/Data/Encoder_data/Test_2/Raw_json/"
# processed_path_1 = "D:/Projekti/Ball_And_Beam/System_Identification/Data/Encoder_data/Test_2/Processed/"

path_1 = "D:/Projekti/Ball_And_Beam/System_Identification/Data/Encoder_data/Test_2/Test_45/Raw_json/"
processed_path_1 = "D:/Projekti/Ball_And_Beam/System_Identification/Data/Encoder_data/Test_2/Test_45/Processed/"


exp_value_1 = [-45, -30, -20, -10, 10, 20, 30, 45]

j = -1

'''
Odredjivanje Relativne greske
'''
for i in range(15):
    if not i%5:
        j = j + 1
    try:
        # Load data
        output_data_path = path_1 + "Test_" + str(i)  + ".json"
        df = pd.read_json(output_data_path)

        # Convert data
        df["Angles"] = df["Counts"]*360.0/600.0
        time_s = df["Time"].to_numpy()
        df["Time_s"] = np.round(time_s/1000000, 2)
        # df["PWM"] = np.full(len(df["Angles"]), exp_value_1[j])
        df.drop("Time", axis=1, inplace=True)
        df.drop("Counts", axis=1, inplace=True)
        df.to_csv(path_1 + "Test_" + str(i) + ".csv")

        show_plot(time_s=df["Time_s"], angle=df["Angles"], idx=i, pwm=df["PWM"])

    except:
        print("Data not found or relevant")
