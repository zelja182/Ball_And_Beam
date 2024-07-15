import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



def show_plot(time_s, angle, pwm, idx):
    plt.figure(idx)
    plt.plot(time_s, angle, time_s, pwm)
    plt.grid()
    plt.title("Test " + str(idx))
    plt.xlabel("Time [s]")
    plt.ylabel("Angle")
    plt.show()


path_1 = "C:/Users/zracic/Documents/Master/Servo_motor_model_identification/Data/Encoder_data/Test_2/Processed/"

for i in range(30):
    try:
        # Load data 
        output_data_path = path_1 + "Test_" + str(i)  + ".csv"
        df = pd.read_csv(output_data_path)
        show_plot(time_s=df["Time_s"], angle=df["Angles"], idx=i, pwm=df["PWM"])
    except Exception as e:
        print(e)
        