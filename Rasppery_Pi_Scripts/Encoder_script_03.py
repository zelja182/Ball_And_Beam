from Scripts import rotary_encoder
import pigpio
import time as t
import json


BUTTON_PIN = 23   # GPIO PIN
LED_PIN = 14      # GPIO PIN
channel_A = 20    # GPIO PIN
channel_B = 21    # GPIO PIN

position = 0 
position_array = []
time_array = []
time_start = 0
test_count = 0

def save_data():
    global test_count
    path = "/home/zelja182/Master Rad/Test_data/Test_"

    data = {
                "Counts" : position_array,
                "Time" : time_array,
            }
    with open(path + str(test_count) + ".json", "w") as f:
        json.dump(data, f)
    test_count = test_count + 1

def var_reset():
    global position
    global position_array
    global time_array
    position = 0
    position_array.clear()
    time_array.clear()
    

def callback(way): 
    global timer_start 
    global position
    position += way
    if len(position_array) == 0:
        timer_start = t.monotonic_ns()
        time_array.append(0)
        position_array.append(position)
    else: 
        time_array.append(t.monotonic_ns() - timer_start)

pi = pigpio.pi() 
decoder = rotary_encoder.decoder(pi, channel_A, channel_B, callback) 
pi.set_mode(BUTTON_PIN, pigpio.INPUT)
pi.set_pull_up_down(BUTTON_PIN, pigpio.PUD_UP)
pi.set_mode(LED_PIN, pigpio.OUTPUT)

while True: 
    if not pi.read(BUTTON_PIN):
        pi.write(LED_PIN, 1)
        t.sleep(1)        
        print(max(position_array))
        save_data()
        var_reset()
        pi.write(LED_PIN, 0)
