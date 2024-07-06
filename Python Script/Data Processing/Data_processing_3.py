import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def separate_data(delay_2:int, data=pd.DataFrame(), delay_1 = 0):
    # return data[data["Time_s"]].between(delay_1/1000, delay_2/1000)
    return data.query(str(delay_1/1000) + "<= Time_s < " + str(delay_2/1000))
    # return data[(data[data["Time_s"]] > delay_1/1000) & (data[["Time_s"]< delay_2/1000])]

def import_missing_values(new_angles, new_time):
    for j in range(1, len(new_time)-1):
        razlika = new_time[j+1] - new_time[j]
        razlika = np.round(razlika, decimals=3)
        if razlika > 0.05:
            missing_time = np.arange(start=np.round(new_time[j], decimals=3), stop=new_time[j+1], step=0.01)
            missing_angles = np.full(shape=np.shape(missing_time), fill_value=new_angles[j])
            new_angles = np.insert(new_angles, j+1, missing_angles)
            new_time = np.insert(new_time, j+1, missing_time)
    return new_angles, new_time

# # Zakomentarisina putevi do direktorijuma za svaki slucaj
path_raw = "D:/Projekti/Za master rad/Servo_motor_model_identification/Data/Encoder_data/Test_3/Test_15/Raw/"
path_input = "D:/Projekti/Za master rad/Servo_motor_model_identification/Data/Encoder_data/Test_3/Test_15/Input_data.json"
path_processed = "D:/Projekti/Za master rad/Servo_motor_model_identification/Data/Encoder_data/Test_3/Test_15/Processed/"


'''
Sredjivanje podataka za Identifikaciju
'''
for i in range(10):
    try:
        # Load data 
        output_data_path = path_raw + "Test_" + str(i)  + ".json"
        df = pd.read_json(output_data_path)

        # Load input data 
        df_in = pd.read_json(path_input)
        input_angles = np.array(df_in["test_" + str(i)]['angle'])
        delays = np.array(df_in["test_" + str(i)]['delay'])
        # adding missing values
        input_angles = np.append(input_angles, 90) 
        delays = np.append(delays, 500)
        del df_in

        # Convert data
        df["Angles"] = df["Counts"]*360.0/600.0
        df["Time_s"] = df["Time"]/1000000000
        df["Time_s"] = df["Time_s"].round(decimals=3)
        df =df.drop(["Counts", "Time"], axis=1)


        # Separate data between delays
        # delay_sum = 0
        # for idx in range(len(delays)):
        #     delay_sum = delay_sum + delays[idx]
        #     match idx:                
        #         case 0:
        #             df_0 = separate_data(data=df, delay_1=delay_sum-delays[idx], delay_2=delay_sum)
        #             new_row = {"Angles": df_0["Angles"].iloc[-1], "Time_s": delay_sum/1000}
        #             df_0.loc[df_0.index[-1]+1] = new_row              
        #             new_angles, new_time = import_missing_values(new_time=df_0["Time_s"].to_numpy(), new_angles=df_0["Angles"].to_numpy())
        #             pwm = np.full((len(new_time)), input_angles[idx] - 90)
        #             pwm[-1] = input_angles[idx+1] - 90
        #             df_10 = pd.DataFrame()
        #             df_10["Angles"] = new_angles
        #             df_10["Time_s"] = new_time
        #             df_10["PWM"] = pwm
        #             del df_0, new_angles, new_time, pwm  
        #         case 1:
        #             df_1 = separate_data(data=df, delay_1=delay_sum-delays[idx], delay_2=delay_sum)
        #             new_row = {"Angles": df_1["Angles"].iloc[-1], "Time_s": delay_sum/1000}
        #             df_1.loc[df_1.index[-1]+1] = new_row              
        #             new_angles, new_time = import_missing_values(new_time=df_1["Time_s"].to_numpy(), new_angles=df_1["Angles"].to_numpy())
        #             pwm = np.full((len(new_time)), input_angles[idx] - 90)
        #             pwm[-1] = input_angles[idx+1] - 90
        #             df_11 = pd.DataFrame()
        #             df_11["Angles"] = new_angles
        #             df_11["Time_s"] = new_time
        #             df_11["PWM"] = pwm
        #             del df_1, new_angles, new_time, pwm             
        #         case 2:
        #             df_2 = separate_data(data=df, delay_1=delay_sum-delays[idx], delay_2=delay_sum)
        #             new_row = {"Angles": df_2["Angles"].iloc[-1], "Time_s": delay_sum/1000}
        #             df_2.loc[df_2.index[-1]+1] = new_row              
        #             new_angles, new_time = import_missing_values(new_time=df_2["Time_s"].to_numpy(), new_angles=df_2["Angles"].to_numpy())
        #             pwm = np.full((len(new_time)), input_angles[idx] - 90)
        #             pwm[-1] = input_angles[idx+1] - 90
        #             df_12 = pd.DataFrame() 
        #             df_12["Angles"] = new_angles
        #             df_12["Time_s"] = new_time
        #             df_12["PWM"] = pwm
        #             del df_2, new_angles, new_time, pwm                
        #         case 3:
        #             df_3 = separate_data(data=df, delay_1=delay_sum-delays[idx], delay_2=delay_sum)
        #             new_row = {"Angles": df_3["Angles"].iloc[-1], "Time_s": delay_sum/1000}
        #             df_3.loc[df_3.index[-1]+1] = new_row           
        #             new_angles, new_time = import_missing_values(new_time=df_3["Time_s"].to_numpy(), new_angles=df_3["Angles"].to_numpy())
        #             pwm = np.full((len(new_time)), input_angles[idx] - 90)
        #             pwm[-1] = input_angles[idx+1] - 90
        #             df_13 = pd.DataFrame()
        #             df_13["Angles"] = new_angles
        #             df_13["Time_s"] = new_time
        #             df_13["PWM"] = pwm
        #             del df_3, new_angles, new_time, pwm               
        #         case 4:
        #             df_4 = separate_data(data=df, delay_1=delay_sum-delays[idx], delay_2=delay_sum)
        #             new_row = {"Angles": df_4["Angles"].iloc[-1], "Time_s": delay_sum/1000}
        #             df_4.loc[df_4.index[-1]+1] = new_row              
        #             new_angles, new_time = import_missing_values(new_time=df_4["Time_s"].to_numpy(), new_angles=df_4["Angles"].to_numpy())
        #             pwm = np.full((len(new_time)), input_angles[idx] - 90)
        #             pwm[-1] = input_angles[idx+1] - 90
        #             df_14 = pd.DataFrame()
        #             df_14["Angles"] = new_angles
        #             df_14["Time_s"] = new_time
        #             df_14["PWM"] = pwm
        #             del df_4, new_angles, new_time, pwm                    
        #         case 5:
        #             df_5 = separate_data(data=df, delay_1=delay_sum-delays[idx], delay_2=delay_sum)
        #             new_row = {"Angles": df_5["Angles"].iloc[-1], "Time_s": delay_sum/1000}
        #             df_5.loc[df_5.index[-1]+1] = new_row              
        #             new_angles, new_time = import_missing_values(new_time=df_5["Time_s"].to_numpy(), new_angles=df_5["Angles"].to_numpy())
        #             pwm = np.full((len(new_time)), input_angles[idx] - 90)
        #             pwm[-1] = input_angles[idx+1] - 90
        #             df_15 = pd.DataFrame()
        #             df_15["Angles"] = new_angles
        #             df_15["Time_s"] = new_time
        #             df_15["PWM"] = pwm
        #             del df_5, new_angles, new_time, pwm     
        #         case 6:
        #             df_6 = separate_data(data=df, delay_1=delay_sum-delays[idx], delay_2=delay_sum)
        #             new_row = {"Angles": df_6["Angles"].iloc[-1], "Time_s": delay_sum/1000}
        #             df_6.loc[df_6.index[-1]+1] = new_row              
        #             new_angles, new_time = import_missing_values(new_time=df_6["Time_s"].to_numpy(), new_angles=df_6["Angles"].to_numpy())
        #             pwm = np.full((len(new_time)), input_angles[idx] - 90)
        #             df_16 = pd.DataFrame()
        #             df_16["Angles"] = new_angles
        #             df_16["Time_s"] = new_time
        #             df_16["PWM"] = pwm
        #             del df_6, new_angles, new_time, pwm                       
        # del df
        
        # # Making new dataframework 
        # df_new = pd.concat([df_10, df_11, df_12, df_13, df_14, df_15, df_16], ignore_index=True)
        # df_new.round(decimals=3)
        
        # plt.figure(i)
        # plt.plot(df_new["Time_s"], df_new["Angles"], df_new["Time_s"], df_new["PWM"])
        # plt.grid()
        # plt.xlabel("Time [s]")
        # plt.ylabel("Angle")
        # plt.show()

        # df_new.to_csv(path_processed + "Test_" + str(i) + ".csv")
        df.to_csv(path_processed + "Test_" + str(i) + ".csv")

    except Exception as e:
        print("Something went wrong!!!")
        print(e)
