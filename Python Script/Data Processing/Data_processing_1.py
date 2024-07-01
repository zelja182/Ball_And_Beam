import pandas as pd
import numpy as np


# # Zakomentarisina putevi do direktorijuma za svaki slucaj
# path_raw = "D:/Projekti/Za master rad/Servo_motor_model_identification/Data/Encoder_data/Test_1/Raw/"
# path_processed = "D:/Projekti/Za master rad/Servo_motor_model_identification/Data/Encoder_data/Test_1/Processed/"
relativ_error = np.zeros((4, 5))
relativ_error_1 = np.zeros((6, 5))
exp_value = [30, 45, 60, 90]
exp_value_1 = [-60, -45, -30, 30, 45, 60]

j = -1

'''
Sredjivanje podataka za Identifikaciju
'''
i = 14
for i in range(20):
    if not i%5:
        j = j + 1
    try:
        # Load data 
        output_data_path = path_raw + "Test_" + str(i)  + ".json"
        df = pd.read_json(output_data_path)

        if df["Counts"][0] == 0:
            df["Counts"] = df["Counts"] + 1
        elif abs(df["Counts"][0]) > abs(df["Counts"][1]):
            df["Counts"] = df["Counts"] + abs(df["Counts"][0]) + 1

        # Convert data
        df["Angles"] = df["Counts"]*360.0/600.0
        df["Time_s"] = df["Time"]/1000000000
        df["Time_s"] = df["Time_s"].round(decimals=3)

        print("data_" + str(i) + ": " + str(df["Time_s"].is_unique))  # Provera da li ima duplikata u koloni za vreme

        df_2 = df[df["Time_s"]<2.0]  # Data before 2.0 sec
        df_3 = df[df["Time_s"]>2.0]  # Data after 2.0 sec
        df_2 =df_2.drop(["Counts", "Time"], axis=1)
        df_3 =df_3.drop(["Counts", "Time"], axis=1)

        # Corect start time and start Angle value
        new_angles = df_2["Angles"].to_numpy()
        new_time = df_2["Time_s"].to_numpy()

        # Provera da li ima velike razlike izmedju t[i] i t[i+1]
        # Ako ima velike razlike, popuni podatke koji nedostaju
        for idx in range(len(new_time)-1):
            razlika = new_time[idx+1] - new_time[idx]
            razlika = np.round(razlika, decimals=3)
            if razlika > 0.1:
                missing_time = np.arange(start=np.round(new_time[idx], decimals=2), stop=new_time[idx+1], step=0.01)
                missing_angles = np.full(shape=np.shape(missing_time), fill_value=new_angles[idx])
                new_angles = np.insert(new_angles, idx+1, missing_angles)
                new_time = np.insert(new_time, idx+1, missing_time)

        new_angles = np.insert(new_angles, 0, 0)  # Dodaj nultu pocetnu vrednos
        new_time = np.append(new_time, new_time[-1]*2 - new_time[-2])  # Dodaj vreme koje nedostaje

        # Formiranje podataka do t = 2.0
        df_21 = pd.DataFrame()
        df_21["Angles"] = new_angles
        df_21["Time_s"] = new_time

        # Dodavanje podataka izmedju t[zadnji ocitan ugao] i t = 2.0
        if (df_3["Time_s"].iloc[0] - df_21["Time_s"].iloc[-1]) > 0.001:
            start = df_21["Time_s"].iloc[-1]
            start = np.round(start, decimals=2)
            time = np.arange(start=start+0.01, stop=2.01, step=0.01)
            angle = np.full(shape=np.shape(time), fill_value=df_21["Angles"].iloc[-1])
        else:
            angle = df_21["Angles"].iloc[-1]
            time = 2.0

        Data = {"Time_s": time, "Angles": angle}
        if np.isscalar(Data["Angles"]):
            df_4 = pd.DataFrame(data=Data, index=[0])
        else:
            df_4 = pd.DataFrame(data=Data)


        # Making new dataframework 
        df_5 = pd.concat([df_21, df_4, df_3], ignore_index=True)
        
        pwm_angle = np.full((len(df_21))+len(df_4)-1, exp_value[j])
        pwm_0 = np.full((len(df_3)+1), 0)
        pwm = np.concatenate((pwm_angle, pwm_0))

        df_5["PWM"] = pwm
        df_5.to_csv(path_processed + "Test_" + str(i) + ".csv")
    except Exception as e:
        print("Something went wrong!!!")
        print(e)
