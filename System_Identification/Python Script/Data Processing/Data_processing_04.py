import pandas as pd
from random import randint
import matplotlib.pyplot as plt


def get_merge_list():
    radnom_list = []
    i = 0

    while i < 13:
        x = randint(0, 17)

        if x not in radnom_list:
            radnom_list.append(x)
            i = i + 1

    for r in radnom_list:
        if r > 8:
            print("Dir_2/Val_Data_" + str(r - 9))
        else:
            print("Dir_1/Val_Data_ " + str(r))




data_path = "../Ball_And_Beam/System_Identification/Data/Encoder_data/Validation_data/"

merge_list = ['Dir_1/Val_Data_6.csv', 'Dir_1/Val_Data_5.csv', 'Dir_1/Val_Data_0.csv', 'Dir_1/Val_Data_8.csv', 'Dir_2/Val_Data_8.csv', 'Dir_2/Val_Data_6.csv', 'Dir_2/Val_Data_2.csv', 
              'Dir_2/Val_Data_4.csv', 'Dir_2/Val_Data_1.csv', 'Dir_2/Val_Data_3.csv', 'Dir_2/Val_Data_0.csv', 'Dir_1/Val_Data_4.csv', 'Dir_1/Val_Data_3.csv']

merge_list_2 = ['Dir_1/Val_Data_1.csv', 'Dir_1/Val_Data_2.csv', 'Dir_1/Val_Data_7.csv', 'Dir_2/Val_Data_5.csv', 'Dir_2/Val_Data_7.csv']



test_data = pd.DataFrame()

for i in range(len(merge_list)):
    df = pd.read_csv(data_path+merge_list[i])
    test_data = pd.concat([test_data, df], ignore_index=True)

test_data.to_csv(data_path + "TestData.csv")

test_data.plot(y=['PWM','Angles'], use_index=True)
plt.show()


validatin_data = pd.DataFrame()

for i in range(len(merge_list_2)):
    df = pd.read_csv(data_path+merge_list_2[i])
    validatin_data = pd.concat([validatin_data, df], ignore_index=True)

validatin_data.to_csv(data_path + "ValidationData.csv")
validatin_data.plot(y=['PWM','Angles'], use_index=True)
plt.show()
