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
    fig_manager = plt.get_current_fig_manager()
    fig_manager.full_screen_toggle()
    plt.show()


def add_missing_data(data_1, data_2):
    # Add missing data
    missing_time = np.arange(start=data_1["Time_s"].iloc[-1]+0.01, stop=data_2["Time_s"].iloc[0], step=0.01)
    if np.equal(np.round(missing_time[-1], 2), data_2["Time_s"].iloc[0]):
        missing_time = np.delete(missing_time, -1)
    missing_time = np.round(missing_time, 2)
    missing_angle = np.full(shape=np.shape(missing_time), fill_value=data_1["Angles"].iloc[-1])
    missing_pwm = np.full(shape=np.shape(missing_time), fill_value=data_1["PWM"].iloc[0])

    # Create tmp DF with missing data
    df_tmp = pd.DataFrame()
    df_tmp["Angles"] = missing_angle
    df_tmp["Time_s"] = missing_time
    df_tmp["PWM"] = missing_pwm

    return df_tmp


path_1 = "D:/Projekti/Ball_And_Beam/System_Identification/Data/Encoder_data/Test_3/Test_30/"
processed_path_1 = "D:/Projekti/Ball_And_Beam/System_Identification/Data/Encoder_data/Test_3/Test_30/Processed/"


for i in range(10):
    try:
        # Load data
        output_data_path = path_1 + "Test_" + str(i) + ".csv"
        df = pd.read_csv(output_data_path)

        pwm = df["PWM"].unique()
        pwm = pwm[~np.isnan(pwm)]

        # Separate data by PWM
        new_data = {}
        for p, idx in zip(pwm, range(len(pwm))):
            new_data[idx * 2] = df.query("PWM ==" + str(p))

        # Add missing data
        for idx in range(len(new_data) - 1):
            new_data[idx * 2 + 1] = add_missing_data(data_1=new_data[idx * 2], data_2=new_data[idx * 2 + 2])

        # Create new data by merging missing data and recorded data
        df_new = pd.DataFrame()
        for idx in range(len(new_data)):
            df_new = pd.concat([df_new, new_data[idx]], ignore_index=True)

        df_new.to_csv(processed_path_1 + "Test_" + str(i) + ".csv")

        show_plot(time_s=df_new["Time_s"], angle=df_new["Angles"], idx=i, pwm=df_new["PWM"])


    except:
        print("Data not found or relevant")
