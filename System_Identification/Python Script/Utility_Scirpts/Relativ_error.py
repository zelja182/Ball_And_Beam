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


# path_1 = "D:/Projekti/Ball_And_Beam/System_Identification/Data/Encoder_data/Test_2/Raw_json/"
# processed_path_1 = "D:/Projekti/Ball_And_Beam/System_Identification/Data/Encoder_data/Test_2/Processed/"

path_1 = "D:/Projekti/Ball_And_Beam/System_Identification/Data/Encoder_data/Test_3/Test_30/Raw_json/"
processed_path_1 = "D:/Projekti/Ball_And_Beam/System_Identification/Data/Encoder_data/Test_3/Test_30/"

relativ_error = np.zeros((4, 5))
relativ_error_1 = np.zeros((6, 5))
exp_value = [30, 45, 60, 90]
exp_value_1 = [-30, -20, -10, 10, 20, 30]

j = -1

'''
Odredjivanje Relativne greske
'''
for i in range(20):
    if not i%5:
        j = j + 1
    try:
        # Load data 
        # output_data_path = path_1 + "Test_" + str(i)  + ".json"
        output_data_path = processed_path_1 + "Test_" + str(i) + ".csv"
        # df = pd.read_json(output_data_path)
        df = pd.read_csv(output_data_path)
        # Convert data
        # df["Angles"] = df["Counts"]*360.0/600.0
        # time_s = df["Time"].to_numpy()
        # df["Time_s"] = np.round(time_s/1000000, 2)
        # df["PWM"] = np.full(len(df["Angles"]), exp_value_1[j])
        # df.drop("Time", axis=1, inplace=True)
        # df.drop("Counts", axis=1, inplace=True)
        # df.to_csv(path_1 + "Test_" + str(i) + ".csv")


        # brake_poit = get_brake_point(df)
        #
        # df_2 = df[:brake_poit]
        # df_3 = df[brake_poit:]
        #
        # miss_value = int(df_3["Time_s"].iloc[0] * 100) - int(df_2["Time_s"].iloc[-1] * 100)
        # missed_angle = np.full(miss_value, df_2["Angles"].iloc[-1])
        # missed_time = np.round(np.linspace(df_2["Time_s"].iloc[-1] + 0.01, df_3["Time_s"].iloc[0] - 0.01, miss_value), 2)
        #
        # df_23 = pd.DataFrame()
        # df_23["Time_s"] = missed_time
        # df_23["Angles"] = missed_angle
        #
        # df_2["PWM"] = np.full(len(df_2["Angles"]), exp_value_1[j])
        # df_23["PWM"] = np.full(len(df_23["Angles"]), exp_value_1[j])
        # df_3["PWM"] = np.full(len(df_3["Angles"]), 0)
        #
        # df_final = pd.concat([df_2, df_23, df_3], ignore_index=True)

        # df_final.to_csv(processed_path_1 + "Test_" + str(i) + ".csv")

        show_plot(time_s=df["Time_s"], angle=df["Angles"], idx=i, pwm=df["PWM"])

        # show_plot(time_s=df_final["Time_s"], angle=df_final["Angles"], idx=i, pwm=df_final["PWM"])
    except:
        print("Data not found or relavant")
        relativ_error[j][i%5] = np.nan

print("Matrica relativnih gresaka:")
print(relativ_error)