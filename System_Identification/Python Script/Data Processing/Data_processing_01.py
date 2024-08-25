import pandas as pd
import numpy as np




tmp_path = "../Ball_And_Beam/System_Identification/Data/Encoder_data/Test_2/Raw/tmp/"
processed_path = "../Ball_And_Beam/System_Identification/Data/Encoder_data/Test_2/Processed/"

for i in range(30):
    try:
        # Load data
        df = pd.read_csv(tmp_path + "Test_" + str(i) + ".csv")

        # Sepertate data
        df_1 = df.query("PWM ==" + str(df["PWM"].iloc[0]))
        df_3 = df.query("PWM ==" + str(df["PWM"].iloc[-1]))
        
        # Add missing data
        missing_time = np.arange(start=df_1["Time_s"].iloc[-1]+0.01, stop=df_3["Time_s"].iloc[0], step=0.01)
        missing_angle = np.full(shape=np.shape(missing_time), fill_value=df_1["Angles"].iloc[-1])
        missing_pwm = np.full(shape=np.shape(missing_time), fill_value=df_1["PWM"].iloc[0])

        # Create new DF with missing data
        df_2 = pd.DataFrame()
        df_2["Angles"] = missing_angle
        df_2["Time_s"] = missing_time
        df_2["PWM"] = missing_pwm

        # Create new DF from 3 separated DFs
        df_new = pd.concat([df_1, df_2, df_3], ignore_index=True)

        # Process and save new DF
        df_new["Time_s"]= df_new["Time_s"].round(decimals=2)
        df_new.drop_duplicates(subset='Time_s', keep='first', inplace=True, ignore_index=True)
        df_new.to_csv(processed_path + "Test_" + str(i) + ".csv")

    except Exception as e:
        print("Something whent wrong!!!")
        print(e)

        