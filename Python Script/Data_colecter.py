import serial
import os

def read_arduiono_data(): 
    data = arduino.readline() 
    return data 

def save_data(test_no = 0):
    dir_path = "D:/Projekti/Za master rad/Servo_motor_model_identification/Data/Input_data"
    file_name = "/Test_input_data_"
    # file_no = len(os.listdir(dir_path + str(test_no)))
    final_path = dir_path + file_name + str(test_no) + ".txt"
    with open(final_path, "w+") as file:
                for d in data_array:
                    file.write(d)

arduino = serial.Serial(port='COM3', baudrate=115200, timeout=.1) 
data_array = []

# dir_path = "D:/Projekti/Za master rad/Servo_motor_model_identification/Data/Input_data"
# test_no = 3
# file_name = "/Test_input_data_"
# file_no = len(os.listdir(dir_path + str(test_no)))
# final_path = dir_path + str(test_no) + file_name + str(file_no) + ".txt"

while True: 
    data = read_arduiono_data()
    data = data.decode("utf-8")  
    try:
        if data.startswith("The end of test"):
            print(data)
            save_data()
            print("Data saved...")
            exit()
        elif data:
            print(data)
            data_array.append(data)            
    except Exception as e:
        print(e)
