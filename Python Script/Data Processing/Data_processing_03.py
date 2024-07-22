import pandas as pd
import numpy as np


path_1 = "../Servo_motor_model_identification/Data/Encoder_data/Test_3/Test_30/Processed/Test_"
val_path_1 = "../Servo_motor_model_identification/Data/Encoder_data/Validation_data/Dir_1/Val_Data_"

path_2 = "../Servo_motor_model_identification/Data/Encoder_data/Test_3/Test_45/Processed/Test_"
val_path_2 = "../Servo_motor_model_identification/Data/Encoder_data/Validation_data/Dir_2/Val_Data_"

for i in range(10):
    try:
        df = pd.read_csv(path_2 + str(i) + ".csv")
        # Process and save new DF
        df["Time_s"]= df["Time_s"].round(decimals=2)
        df.drop_duplicates(subset='Time_s', keep='first', inplace=True, ignore_index=True)
        df.to_csv(val_path_2 + str(i) + ".csv")
    except Exception as e:
        print(e)