import serial

arduino = serial.Serial(port='COM3', baudrate=115200, timeout=0.1)

# print(bytes('0', 'utf-8'))
# angle = "180"
# angle_for_arduino = angle.encode('utf-8')
# print("Write")
# print(angle_for_arduino)
# # arduino.write(angle_for_arduino)


# print("\nRead")
# arduino.write(b'180')
# print(arduino.read().decode('utf-8'))
# print(arduino.read().decode('utf-8'))

while True:
    ulaz = input("Daj neki tekst: ")
    # for i in ulaz:
    # arduino.write(bytes(ulaz, 'askii'))
    arduino.write(ulaz.encode(encding='askii'))
    # print(ulaz)
    print(ulaz.encode(encoding='askii'))
    # print(bytes(ulaz, encoding='utf-8'))
    print(arduino.read())
