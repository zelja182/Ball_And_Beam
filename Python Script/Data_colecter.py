import serial

def read_arduiono_data(): 
    data = arduino.readline() 
    return data 


arduino = serial.Serial(port='COM3', baudrate=115200, timeout=.1) 
data_array = []

while True: 
    data = read_arduiono_data()
    data = data.decode("utf-8")  
    try:
        if data.startswith("The end of test"):
            print(data_array)
        elif data:
            print(data)
            data_array.append(data)            
    except Exception as e:
        print(e)
