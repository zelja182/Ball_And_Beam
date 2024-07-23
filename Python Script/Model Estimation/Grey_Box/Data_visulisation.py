import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


path = "../Servo_motor_model_identification/Data/Estimation_data/Grey_Box.csv"
df = pd.read_csv(path)

df = df.drop(columns=['test', 'a', 'b', 'mse-0-6', 'mse-1-6'])

plt.style.use('_mpl-gallery')

# make data:
np.random.seed(10)

# plot
fig, ax = plt.subplots()
ax.set_title("MSE Data Visualisation")
VP = ax.boxplot(df, widths=0.2, patch_artist=True,
                showmeans=False, showfliers=False,
                medianprops={"color": "white", "linewidth": 0.5},
                boxprops={"facecolor": "C0", "edgecolor": "white",
                          "linewidth": 0.5},
                whiskerprops={"color": "C0", "linewidth": 1.5},
                capprops={"color": "C0", "linewidth": 1.5})

# x_data = np.full(shape=len(df["mse-0-0"]), fill_value='mse-0-0')
# ax.scatter(x=x_data, y=df['mse-0-0'])
ax.violinplot(df, widths=0.5, showmeans=False, showmedians=False, showextrema=False)

ax.set_xticklabels(df.columns)


plt.show()