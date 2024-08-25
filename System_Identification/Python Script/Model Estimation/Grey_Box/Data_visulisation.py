import matplotlib.pyplot as plt
import pandas as pd

matlab_data_path = "../Servo_motor_model_identification/Data/Estimation_data/GreyBox/Matlab/Est_data_1.json"
python_data_path_1 = "../Servo_motor_model_identification/Data/Estimation_data/GreyBox/Python/Est_data.csv"
python_data_path_2 = "../Servo_motor_model_identification/Data/Estimation_data/GreyBox/Python/Est_data_1.csv"


def workaround():
    '''
    There are few steps that should be followed
    1. Open matlab_data_path
    2. Use online JSON formater and format data to look pretty
    3. Replace --> "MSE": with --> blank line
    4. Replace --> }, with --> ,
    5. Remove last }
    6. Use online JSON formater to make data pretty one more time
    7. Use workaround script to translate data and then save it as .csv at this python_data_path_1
    8. 1st column doesn't have name, --> add name 'test_no'
    After all of this steps, we are ready to use this data and show some plots 
    '''
    df = pd.read_json(matlab_data_path)
    df = df.T
    df.to_csv(python_data_path_1)


def show_plot():
    '''
    This function will show you some graph 
    '''
    df = pd.read_csv(python_data_path_1)  

    df = df.drop(columns=['test_no','num', 'den'])

    plt.style.use('_mpl-gallery')

    # plot
    _, ax = plt.subplots()
    ax.set_title("MSE Data Visualisation")
    VP = ax.boxplot(df, widths=0.2, patch_artist=True,
                    showmeans=False, showfliers=False,
                    medianprops={"color": "white", "linewidth": 0.5},
                    boxprops={"facecolor": "C0", "edgecolor": "white",
                            "linewidth": 0.5},
                    whiskerprops={"color": "C0", "linewidth": 1.5},
                    capprops={"color": "C0", "linewidth": 1.5})


    ax.violinplot(df, widths=0.5, showmeans=False, showmedians=False, showextrema=False)
    ax.set_xticklabels(df.columns)

    plt.show()

def make_new_table(colums_to_drop):
    '''
    This function will make new table with out outliers and show the best match for TF
    '''
    df = pd.read_csv(python_data_path_1)  
    df = df.drop(columns=colums_to_drop)   
    cols_to_sum = df.columns.to_list()
    for i in range(3):
        cols_to_sum.pop(0)
    df['avg_mse'] = df[cols_to_sum].sum(axis=1)/len(cols_to_sum)
    print(df.loc[df["avg_mse"] == df["avg_mse"].min()])
    df.to_csv(python_data_path_2)


if __name__=="__main__":
    # workaround()
    # show_plot()
    make_new_table(['mse_2_4', 'mse_2_5', 'mse_2_7', 'mse_2_9'])

