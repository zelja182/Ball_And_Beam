import pandas as pd
import matplotlib.pyplot as plt

def merge(start, end):
    # path_1 = "../Ball_And_Beam/System_Identification/Data/Encoder_data/Test_1/Processed/"
    path_1 = "../Ball_And_Beam/System_Identification/Data/Encoder_data/Test_2/Processed/"  # uncoment for test 2 
    df_2 = pd.DataFrame()
    for i in range(start, end):
        output_data_path = path_1 + "Test_" + str(i)  + ".csv"
        df = pd.read_csv(output_data_path)
        ang_name = "Angles_" + str(i%5)
        t_name = "Time_" + str(i%5)

        df_2[ang_name] = df["Angles"]
        df_2[t_name] = df["Time_s"]
        df_2["PWM"] = df['PWM']
    return df_2

# fig_title = "Експеримент 1"
fig_title = "Експеримент 2"  # uncoment for test 2 
df_n60 = merge(start=0, end=5)
df_n45 = merge(start=5, end=10)
df_n30 = merge(start=10, end=15)
df_30 = merge(start=15, end=20)
df_45 = merge(start=20, end=25)  # uncoment for test 2
df_60 = merge(start=25, end=30)  # uncoment for test 2 


# fig, axs = plt.subplots(4,5)
fig, axs = plt.subplots(6,5)
fig.suptitle(fig_title)
axs[0, 0].plot(df_n60["Time_0"], df_n60["Angles_0"], df_n60["Time_0"], df_n60['PWM'])
axs[0, 1].plot(df_n60["Time_1"], df_n60["Angles_1"], df_n60["Time_1"], df_n60['PWM'])
axs[0, 2].plot(df_n60["Time_2"], df_n60["Angles_2"], df_n60["Time_2"], df_n60['PWM'])
axs[0, 3].plot(df_n60["Time_3"], df_n60["Angles_3"], df_n60["Time_3"], df_n60['PWM'])
axs[0, 4].plot(df_n60["Time_4"], df_n60["Angles_4"], df_n60["Time_4"], df_n60['PWM'])
axs[0,0].set_title(str(int(df_n60['PWM'].iloc[0])) + "$^\circ$")
axs[0,1].set_title(str(int(df_n60['PWM'].iloc[0])) + "$^\circ$")
axs[0,2].set_title(str(int(df_n60['PWM'].iloc[0])) + "$^\circ$")
axs[0,3].set_title(str(int(df_n60['PWM'].iloc[0])) + "$^\circ$")
axs[0,4].set_title(str(int(df_n60['PWM'].iloc[0])) + "$^\circ$")

axs[1, 0].plot(df_n45["Time_0"], df_n45["Angles_0"], df_n45["Time_0"], df_n45['PWM'])
axs[1, 1].plot(df_n45["Time_1"], df_n45["Angles_1"], df_n45["Time_1"], df_n45['PWM'])
axs[1, 2].plot(df_n45["Time_2"], df_n45["Angles_2"], df_n45["Time_2"], df_n45['PWM'])
axs[1, 3].plot(df_n45["Time_3"], df_n45["Angles_3"], df_n45["Time_3"], df_n45['PWM'])
axs[1, 4].plot(df_n45["Time_4"], df_n45["Angles_4"], df_n45["Time_4"], df_n45['PWM'])
axs[1,0].set_title(str(int(df_n45['PWM'].iloc[0])) + "$^\circ$")
axs[1,1].set_title(str(int(df_n45['PWM'].iloc[0])) + "$^\circ$")
axs[1,2].set_title(str(int(df_n45['PWM'].iloc[0])) + "$^\circ$")
axs[1,3].set_title(str(int(df_n45['PWM'].iloc[0])) + "$^\circ$")
axs[1,4].set_title(str(int(df_n45['PWM'].iloc[0])) + "$^\circ$")

# plt.show()

# fig, axs = plt.subplots(2,5)
# fig.suptitle(fig_title)

axs[2, 0].plot(df_n30["Time_0"], df_n30["Angles_0"], df_n30["Time_0"], df_n30['PWM'])
axs[2, 1].plot(df_n30["Time_1"], df_n30["Angles_1"], df_n30["Time_1"], df_n30['PWM'])
axs[2, 2].plot(df_n30["Time_2"], df_n30["Angles_2"], df_n30["Time_2"], df_n30['PWM'])
axs[2, 3].plot(df_n30["Time_3"], df_n30["Angles_3"], df_n30["Time_3"], df_n30['PWM'])
axs[2, 4].plot(df_n30["Time_4"], df_n30["Angles_4"], df_n30["Time_4"], df_n30['PWM'])
axs[2,0].set_title(str(int(df_n30['PWM'].iloc[0])) + "$^\circ$")
axs[2,1].set_title(str(int(df_n30['PWM'].iloc[0])) + "$^\circ$")
axs[2,2].set_title(str(int(df_n30['PWM'].iloc[0])) + "$^\circ$")
axs[2,3].set_title(str(int(df_n30['PWM'].iloc[0])) + "$^\circ$")
axs[2,4].set_title(str(int(df_n30['PWM'].iloc[0])) + "$^\circ$")

axs[3, 0].plot(df_30["Time_0"], df_30["Angles_0"], df_30["Time_0"], df_30['PWM'])
axs[3, 1].plot(df_30["Time_1"], df_30["Angles_1"], df_30["Time_1"], df_30['PWM'])
axs[3, 2].plot(df_30["Time_2"], df_30["Angles_2"], df_30["Time_2"], df_30['PWM'])
axs[3, 3].plot(df_30["Time_3"], df_30["Angles_3"], df_30["Time_3"], df_30['PWM'])
axs[3, 4].plot(df_30["Time_4"], df_30["Angles_4"], df_30["Time_4"], df_30['PWM'])
axs[3,0].set_title(str(int(df_30['PWM'].iloc[0])) + "$^\circ$")
axs[3,1].set_title(str(int(df_30['PWM'].iloc[0])) + "$^\circ$")
axs[3,2].set_title(str(int(df_30['PWM'].iloc[0])) + "$^\circ$")
axs[3,3].set_title(str(int(df_30['PWM'].iloc[0])) + "$^\circ$")
axs[3,4].set_title(str(int(df_30['PWM'].iloc[0])) + "$^\circ$")




# For test 2 uncoment part bellow 


# fig, axs = plt.subplots(2,5)
# fig.suptitle(fig_title)

axs[4, 0].plot(df_45["Time_0"], df_45["Angles_0"], df_45["Time_0"], df_45['PWM'])
axs[4, 1].plot(df_45["Time_1"], df_45["Angles_1"], df_45["Time_1"], df_45['PWM'])
axs[4, 2].plot(df_45["Time_2"], df_45["Angles_2"], df_45["Time_2"], df_45['PWM'])
axs[4, 3].plot(df_45["Time_3"], df_45["Angles_3"], df_45["Time_3"], df_45['PWM'])
axs[4, 4].plot(df_45["Time_4"], df_45["Angles_4"], df_45["Time_4"], df_45['PWM'])
axs[4,0].set_title(str(int(df_45['PWM'].iloc[0])) + "$^\circ$")
axs[4,1].set_title(str(int(df_45['PWM'].iloc[0])) + "$^\circ$")
axs[4,2].set_title(str(int(df_45['PWM'].iloc[0])) + "$^\circ$")
axs[4,3].set_title(str(int(df_45['PWM'].iloc[0])) + "$^\circ$")
axs[4,4].set_title(str(int(df_45['PWM'].iloc[0])) + "$^\circ$")


axs[5, 0].plot(df_60["Time_0"], df_60["Angles_0"], df_60["Time_0"], df_60['PWM'])
axs[5, 1].plot(df_60["Time_1"], df_60["Angles_1"], df_60["Time_1"], df_60['PWM'])
axs[5, 2].plot(df_60["Time_2"], df_60["Angles_2"], df_60["Time_2"], df_60['PWM'])
axs[5, 3].plot(df_60["Time_3"], df_60["Angles_3"], df_60["Time_3"], df_60['PWM'])
axs[5, 4].plot(df_60["Time_4"], df_60["Angles_4"], df_60["Time_4"], df_60['PWM'])
axs[5,0].set_title(str(int(df_60['PWM'].iloc[0])) + "$^\circ$")
axs[5,1].set_title(str(int(df_60['PWM'].iloc[0])) + "$^\circ$")
axs[5,2].set_title(str(int(df_60['PWM'].iloc[0])) + "$^\circ$")
axs[5,3].set_title(str(int(df_60['PWM'].iloc[0])) + "$^\circ$")
axs[5,4].set_title(str(int(df_60['PWM'].iloc[0])) + "$^\circ$")


plt.show()

