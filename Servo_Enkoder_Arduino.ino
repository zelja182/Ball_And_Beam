#include <Servo.h>

Servo my_servo;
int servo_angle;
char buf[80];

int readline(int readch, char *buffer, int len) {
    static int pos = 0;
    int rpos;

    if (readch > 0) {
        switch (readch) {
            case '\r': // Ignore CR
                break;
            case '\n': // Return on new-line
                rpos = pos;
                pos = 0;  // Reset position index ready for next time
                return rpos;
            default:
                if (pos < len-1) {
                    buffer[pos++] = readch;
                    buffer[pos] = 0;
                }
        }
    }
    return 0;
}

void setup() {
  // init
  Serial.begin(9600);
  my_servo.attach(6, 500, 2400);
}

void loop() {
  // put your main code here, to run repeatedly:
  if (readline(Serial.read(), buf, 80) > 0)
   {
    servo_angle = atoi(buf);
    Serial.println(servo_angle);
    my_servo.write(servo_angle);
    Serial.println(my_servo.read());
    }
}
