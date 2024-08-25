import pandas as pd
import numpy as np

def add_missing_data(data_1, data_2):
    # Add missing data
    missing_time = np.arange(start=data_1["Time_s"].iloc[-1]+0.01, stop=data_2["Time_s"].iloc[0], step=0.01)
    missing_angle = np.full(shape=np.shape(missing_time), fill_value=data_1["Angles"].iloc[-1])
    missing_pwm = np.full(shape=np.shape(missing_time), fill_value=data_1["PWM"].iloc[0])

    # Create tmp DF with missing data
    df_tmp = pd.DataFrame()
    df_tmp["Angles"] = missing_angle
    df_tmp["Time_s"] = missing_time
    df_tmp["PWM"] = missing_pwm

    return df_tmp


tmp_path = "../Ball_And_Beam/System_Identification/Data/Encoder_data/Test_3/Test_45/Raw/tmp/"
input_data = "../Ball_And_Beam/System_Identification/Data/Encoder_data/Test_3/Test_45/Input_data.json"
processed_path = "../Ball_And_Beam/System_Identification/Data/Encoder_data/Test_3/Test_45/Processed/"

for i in range(10):
    try:
        df_in = pd.read_json(input_data)
        if df_in['test_'+str(i)]['depricated']:
            print("This data can't be proecessed or requers additional manual action in order to be processed with this script")
        else:
            del df_in
            df = pd.read_csv(tmp_path + "Test_" + str(i) + ".csv", index_col=[0])
            df["Time_s"]= df["Time_s"].round(decimals=3)

            # Separate data
            pwm = df["PWM"].unique()
            new_data = {}
            for p, idx in zip(pwm, range(len(pwm))):
                new_data[idx*2] = df.query("PWM ==" + str(p))

            # Add missing data
            for idx in range(len(new_data)-1):
                new_data[idx*2+1] = add_missing_data(data_1=new_data[idx*2], data_2=new_data[idx*2+2])
            
            # Merge all data frameworks into one
            df_new = pd.DataFrame()
            for idx in range(len(new_data)):
                df_new = pd.concat([df_new, new_data[idx]], ignore_index=True)

            # Save data
            df_new["Time_s"]= df_new["Time_s"].round(decimals=3)
            print("Test {} is unique: {}".format(i, df_new["Time_s"].is_unique))  # Check if Time_s is unique, if not correct it manualy
            df_new.to_csv(processed_path + "Test_" + str(i) + ".csv")

    except Exception as e:
        print("Something whent wrong while proccessing file number: ", i)
        print(e)

        