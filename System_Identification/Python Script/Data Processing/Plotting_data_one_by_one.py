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


processed_path_1 = "D:/Projekti/Ball_And_Beam/System_Identification/Data/Encoder_data/Test_2/Test_30/Processed/"



for i in range(40):
    try:
        # Load data
        output_data_path = processed_path_1 + "Test_" + str(i) + ".csv"
        df = pd.read_csv(output_data_path)

        show_plot(time_s=df["Time_s"], angle=df["Angles"], idx=i, pwm=df["PWM"])

    except:
        print("Data not found or relevant")

