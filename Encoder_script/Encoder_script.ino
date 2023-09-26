#include "Timer.h"

// Encoder set up
// Pin set up
int outputA = 2;
int outputB = 3;
#define readA bitRead(PIND, 2)  //faster than digitalRead()
#define readB bitRead(PIND, 3)  //faster than digitalRead()
// function variables set up
int counter = 0;
int test_counter = 0;
// timer and buffers set up
Timer timer;
int encoder_index = 0;
double angle_values[] = { 1.2 };
unsigned int time_value[] = { 1 };
int total_time = 0;

int servo_test_ready = 4;
int servo_data_ready = 5;
int encoder_test_ready = 7;
int encoder_data_ready = 8;
#define readServo_data bitRead(PIND, servo_data_ready)
#define readServo_test bitRead(PIND, servo_test_ready)

void encoder_function_a();
void encoder_function_b();
void printDouble(double val, unsigned int precision);

void setup() {
  // init
  Serial.begin(115200);
  pinMode(outputA, INPUT_PULLUP);
  pinMode(outputB, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(outputA), encoder_function_a, CHANGE);
  attachInterrupt(digitalPinToInterrupt(outputB), encoder_function_b, CHANGE);

  pinMode(servo_test_ready, INPUT);
  pinMode(servo_data_ready, INPUT);
  pinMode(encoder_test_ready, OUTPUT);
  pinMode(encoder_data_ready, OUTPUT);
}

void loop() {
  if (servo_test_ready && !servo_data_ready) {
    interrupts();
    counter = 0;
    digitalWrite(encoder_test_ready, HIGH);
    timer.start();
  }
  if (servo_data_ready && !servo_test_ready) {
    total_time = timer.read();
    timer.stop();
    noInterrupts();
    digitalWrite(encoder_test_ready, LOW);
    digitalWrite(encoder_data_ready, HIGH);
    Serial.print("Test number: ");
    Serial.println(counter);
    for (int i = 0; i < encoder_index; i++) {
      Serial.print("Angle: ");
      printDouble(angle_values[i], 1000);
      Serial.print("Time: ");
      Serial.println(time_value[i]);
    }
    Serial.print("Total time: ");
    Serial.println(total_time);
    Serial.println("Data transfer finished");
    encoder_index = 0;
    test_counter++;
    digitalWrite(encoder_data_ready, LOW);
  }
}


// Encoder function
void encoder_function_a() {
  if (readB != readA)
    counter++;
  else
    counter--;

  angle_values[encoder_index] = 360.0 * counter / 600.0;
  time_value[encoder_index] = timer.read();
  encoder_index++;
}

void encoder_function_b() {
  if (readA == readB)
    counter++;
  else
    counter--;
  angle_values[encoder_index] = 360.0 * counter / 600.0;
  time_value[encoder_index] = timer.read();
  encoder_index++;
}

// Utilyts
void printDouble(double val, unsigned int precision) {
  Serial.print(int(val));  //prints the int part
  Serial.print(".");       // print the decimal point
  unsigned int frac;
  if (val >= 0)
    frac = (val - int(val)) * precision;
  else
    frac = (int(val) - val) * precision;
  Serial.println(frac, DEC);
}
