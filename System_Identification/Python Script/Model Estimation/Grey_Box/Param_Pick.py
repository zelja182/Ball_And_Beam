import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


dir_path = "../Ball_And_Beam/System_Identification/Data/Estimation_data/"

df = pd.read_csv(dir_path + "Grey_Box.csv")

df_2 = df.drop(columns=['test', 'a', 'b', 'mse-0-6', 'mse-1-6', 'mse-1-5', 'mse-1-7', 'mse-1-9'])

# print(df_2)

df_2['mse_mean'] = df_2.mean(axis=1)

df_3 = pd.DataFrame()

df_3['tst'] = df['test']
df_3['a'] = df['a']
df_3['b'] = df['b']
df_3['mean_mse'] = df_2['mse_mean']

df_3.to_csv(dir_path + "GreyBoxFinal.csv")