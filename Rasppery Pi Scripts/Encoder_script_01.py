import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import time as t
import json

BUTTON_PIN = 16
LED_PIN = 8
ENCODER_PIN_A = 38
ENCODER_PIN_B = 40

path = "/home/zelja182/Master Rad/Test_data/Test_"
test_count = 0

timer_start = 0 
count_var = 0 
count_array = []
time_array = [] 

def var_reset():
    global count_var
    global count_array
    global time_array
    count_var = 0
    count_array = []
    time_array = [] 

def collect_data():
    global timer_start 
    if len(count_array) == 0:
        timer_start = t.monotonic_ns()
        time_array.append(0)
        count_array.append(count_var)
    else: #len(count_array) == 1:
        time_array.append(t.monotonic_ns() - timer_start)
        count_array.append(count_var)
        

def isA(channel):
    global count_var 
    if GPIO.input(ENCODER_PIN_B) != GPIO.input(ENCODER_PIN_A):
        count_var = count_var + 1
    else:
        count_var = count_var - 1
    collect_data()
        
def isB(channel):
    global count_var    
    if GPIO.input(ENCODER_PIN_B) == GPIO.input(ENCODER_PIN_A):
        count_var = count_var + 1
    else:
        count_var = count_var - 1
    collect_data()
        
GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(LED_PIN, GPIO.OUT, initial=GPIO.LOW) # Set pin 8 to be an output pin and set initial value to low (off)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(ENCODER_PIN_A, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(ENCODER_PIN_B, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.add_event_detect(ENCODER_PIN_A, GPIO.BOTH, callback=isA)
GPIO.add_event_detect(ENCODER_PIN_B, GPIO.BOTH, callback=isB)

try: 
    while True: # Run forever
        if GPIO.input(BUTTON_PIN):
            GPIO.output(LED_PIN, GPIO.HIGH) # Turn on
        else:
            print("This is cool")
            GPIO.output(LED_PIN, GPIO.LOW) # Turn off
            
            data = {
                "Counts" : count_array,
                "Time" : time_array,
            }
            with open(path + str(test_count) + ".json", "w") as f:
                json.dump(data, f)
            var_reset()
            test_count = test_count + 1
            t.sleep(1)

except KeyboardInterrupt:
    GPIO.cleanup()
    print("\nExiting...")
