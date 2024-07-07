import pigpio
import time as t
import json
from Scripts import rotary_encoder

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
        "Counts": position_array,
        "Time": time_array,
    }
    with open(path + str(test_count) + ".json", "w") as f:
        json.dump(data, f)
    test_count += 1

def var_reset():
    global position, position_array, time_array
    position = 0
    position_array = []
    time_array = []

def collect_data():
    global time_start
    if not position_array:
        time_start = t.monotonic_ns()
        time_array.append(0)
        position_array.append(position)
    else:
        time_array.append(t.monotonic_ns() - time_start)
        position_array.append(position)

def callback(way):
    global position
    position += way
    collect_data()

def debounce(func, wait_time=0.01):
    last_time = 0

    def debounced_func(*args, **kwargs):
        nonlocal last_time
        current_time = t.time()
        if current_time - last_time >= wait_time:
            last_time = current_time
            return func(*args, **kwargs)
    return debounced_func

pi = pigpio.pi()
decoder = rotary_encoder.decoder(pi, channel_A, channel_B, callback)

pi.set_mode(BUTTON_PIN, pigpio.INPUT)
pi.set_pull_up_down(BUTTON_PIN, pigpio.PUD_UP)
pi.set_mode(LED_PIN, pigpio.OUTPUT)

@debounce
def button_press_handler():
    pi.write(LED_PIN, 1)
    t.sleep(1)
    print(max(position_array))
    save_data()
    var_reset()
    pi.write(LED_PIN, 0)

try:
    while True:
        if not pi.read(BUTTON_PIN):
            button_press_handler()
        t.sleep(0.01)  # Small sleep to avoid busy-waiting

except KeyboardInterrupt:
    print("Exiting...")
finally:
    decoder.cancel()
    pi.stop()
