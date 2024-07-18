import pandas as pd
import numpy as np


path_1 = "../Servo_motor_model_identification/Data/Encoder_data/Test_3/Test_30/Processed/Test_9.csv"
path_2 = "../Servo_motor_model_identification/Data/Encoder_data/Test_3/Test_45/Processed/Test_1.csv"
val_path = "../Servo_motor_model_identification/Data/Encoder_data/Validation_data/"

df = pd.read_csv(path_2)
# Process and save new DF
df["Time_s"]= df["Time_s"].round(decimals=2)
df.drop_duplicates(subset='Time_s', keep='first', inplace=True, ignore_index=True)
df.to_csv(val_path + "Validation_data_2.csv")