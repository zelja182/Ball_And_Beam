import pandas as pd
import matplotlib.pyplot as plt

def merge(start, end):
    path_1 = "../Ball_And_Beam/System_Identification/Data/Encoder_data/Test_1/Processed/"
    df_2 = pd.DataFrame()
    for i in range(start, end):
        output_data_path = path_1 + "Test_" + str(i)  + ".csv"
        df = pd.read_csv(output_data_path)
        ang_name = "Angles_" + str(i%5)
        t_name = "Time_" + str(i%5)

        df_2[ang_name] = df["Angles"]
        df_2[t_name] = df["Time_s"]
    return df_2

fig_title = "Iteracija 1 - PWM = (500, 3000)"
df_30 = merge(start=0, end=5)
df_45 = merge(start=5, end=10)
df_60 = merge(start=10, end=15)
df_90 = merge(start=15, end=20)

fig, axs = plt.subplots(2,5)
fig.suptitle(fig_title)
axs[0, 0].plot(df_30["Time_0"], df_30["Angles_0"])
axs[0, 1].plot(df_30["Time_1"], df_30["Angles_1"])
axs[0, 2].plot(df_30["Time_2"], df_30["Angles_2"])
axs[0, 3].plot(df_30["Time_3"], df_30["Angles_3"])
axs[0, 4].plot(df_30["Time_4"], df_30["Angles_4"])
axs[0,0].set_title("30$^\circ$")
axs[0,1].set_title("30$^\circ$")
axs[0,2].set_title("30$^\circ$")
axs[0,3].set_title("30$^\circ$")
axs[0,4].set_title("30$^\circ$")

axs[1, 0].plot(df_45["Time_0"], df_45["Angles_0"])
axs[1, 1].plot(df_45["Time_1"], df_45["Angles_1"])
axs[1, 2].plot(df_45["Time_2"], df_45["Angles_2"])
axs[1, 3].plot(df_45["Time_3"], df_45["Angles_3"])
axs[1, 4].plot(df_45["Time_4"], df_45["Angles_4"])
axs[1,0].set_title("45$^\circ$")
axs[1,1].set_title("45$^\circ$")
axs[1,2].set_title("45$^\circ$")
axs[1,3].set_title("45$^\circ$")
axs[1,4].set_title("45$^\circ$")

plt.show()

fig, axs = plt.subplots(2,5)
fig.suptitle(fig_title)
axs[0, 0].plot(df_60["Time_0"], df_60["Angles_0"])
axs[0, 1].plot(df_60["Time_1"], df_60["Angles_1"])
axs[0, 2].plot(df_60["Time_2"], df_60["Angles_2"])
axs[0, 3].plot(df_60["Time_3"], df_60["Angles_3"])
axs[0, 4].plot(df_60["Time_4"], df_60["Angles_4"])
axs[0,0].set_title("60$^\circ$")
axs[0,1].set_title("60$^\circ$")
axs[0,2].set_title("60$^\circ$")
axs[0,3].set_title("60$^\circ$")
axs[0,4].set_title("60$^\circ$")

axs[1, 0].plot(df_90["Time_0"], df_90["Angles_0"])
axs[1, 1].plot(df_90["Time_1"], df_90["Angles_1"])
axs[1, 2].plot(df_90["Time_2"], df_90["Angles_2"])
axs[1, 3].plot(df_90["Time_3"], df_90["Angles_3"])
axs[1, 4].plot(df_90["Time_4"], df_90["Angles_4"])
axs[1,0].set_title("90$^\circ$")
axs[1,1].set_title("90$^\circ$")
axs[1,2].set_title("90$^\circ$")
axs[1,3].set_title("90$^\circ$")
axs[1,4].set_title("90$^\circ$")

plt.show()

