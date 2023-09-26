
#include <Servo.h>
#include "Timer.h"

Timer timer;

Servo my_servo;
int servo_angle;
int total_time;
char buf[80];
int random_angles[10];
int random_delay[10];

int servo_test_ready = 4;
int servo_data_ready = 5;
int encoder_test_ready = 7;
int encoder_data_ready = 8;


int test_angles[7] = { 30, 45, 60, 90, 120, 135, 180 };
int random_test_1[13] = { 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1200, 1500, 2000 };
int random_test_2[10] = { 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000 };

#define readEncoder_data bitRead(PIND, encoder_data_ready)
#define readEncoder_test bitRead(PIND, encoder_test_ready)
// test
void standard_test(int tst_angle, int test_no);
void all_random_test(int min_pause, int max_pause, int test_no);
void rnd_angles_const_delay(int pause_time, int test_no);
// untily function
void printDouble(double val, unsigned int precision);
int readline(int readch, char *buffer, int len);




void setup() {
  Serial.begin(115200);
  my_servo.attach(6, 500, 3000);
  my_servo.write(0);
  pinMode(servo_test_ready, OUTPUT);
  pinMode(servo_data_ready, OUTPUT);
  pinMode(encoder_test_ready, INPUT);
  pinMode(encoder_data_ready, INPUT);
}

void loop() {
  // Standard test
  for (int i = 0; i < 7; i++) {
    standard_test(test_angles[i], i);
  }
  // Random angles constant delay
  for (int i = 0; i < 13; i++) {
    rnd_angles_const_delay(random_test_1[i], i);
  }

  for (int i = 0; i < 10; i++) {
    all_random_test(0, random_test_2[i], i);
  }
}

// Test functions
void standard_test(int tst_angle, int test_no) {
  for (int i = 0; i < 1; i++) {
    digitalWrite(servo_test_ready, HIGH);       // Sending to Encoder Arduino that it is ready to start test
    if (readEncoder_test && !readEncoder_data)  // Waiting Encoder Arduino to finish with data transfer and to be ready for test
    {
      //Test time
      timer.start();
      my_servo.write(tst_angle);
      total_time = timer.read();
      timer.stop();

      digitalWrite(servo_test_ready, LOW);        // Sending to Encoder Arduino that test is finished
      digitalWrite(servo_data_ready, HIGH);       // Sending to Encoder Arduino that it is ready for data transfer
      if (readEncoder_data && !readEncoder_test)  // Waiting Encoder Arduino to say it is ready for data transfer
      {
        // Data transfer
        Serial.print("Standard test: ");
        Serial.print(test_no);
        Serial.print(".");
        Serial.println(i);
        Serial.print("Test angle: ");
        Serial.println(tst_angle);
        Serial.print("Total time: ");
        Serial.println(total_time);
        my_servo.write(0);
        delay(1000);
        digitalWrite(servo_data_ready, LOW);  // Sending to Encoder Arduino that data transfer is finished
      }
    }
  }
}

void all_random_test(int min_pause, int max_pause, int test_no) {
  int pause_time;
  for (int i = 0; i < 5; i++) {
    digitalWrite(servo_test_ready, HIGH);       // Sending to Encoder Arduino that it is ready to start test
    if (readEncoder_test && !readEncoder_data)  // Waiting Encoder Arduino to finish with data transfer and to be ready for test
    {
      // Test
      timer.start();
      for (int j = 0; j < 10; j++) {
        servo_angle = random(0, 180);               // Pick random angle
        pause_time = random(min_pause, max_pause);  // Pick random delay

        my_servo.write(servo_angle);

        random_angles[j] = servo_angle;  // Save angle
        random_delay[j] = pause_time;    // Save delay
        delay(pause_time);
      }
      total_time = timer.read();
      timer.stop();

      digitalWrite(servo_test_ready, LOW);        // Sending to Encoder Arduino that test is finished
      digitalWrite(servo_data_ready, HIGH);       // Sending to Encoder Arduino that it is ready for data transfer
      if (readEncoder_data && !readEncoder_test)  // Waiting Encoder Arduino to say it is ready for data transfer
      {
        // Data transfer
        Serial.print("All random test: ");
        Serial.print(test_no);
        Serial.print(".");
        Serial.println(i);
        for (int i = 0; i < 10; i++) {
          Serial.print("Test random angle_");
          Serial.print(i);
          Serial.print(": ");
          Serial.println(random_angles[i]);
          Serial.print("Test random delay_");
          Serial.print(i);
          Serial.print(": ");
          Serial.println(random_delay[i]);
        }
        Serial.print("Total time: ");
        Serial.println(total_time);
        my_servo.write(0);
        delay(1000);
        digitalWrite(servo_data_ready, LOW);  // Sending to Encoder Arduino that data transfer is finished
      }
    }
  }
}

void rnd_angles_const_delay(int pause_time, int test_no) {
  for (int i = 0; i < 5; i++) {
    digitalWrite(servo_test_ready, HIGH);       // Sending to Encoder Arduino that it is ready to start test
    if (readEncoder_test && !readEncoder_data)  // Waiting Encoder Arduino to finish with data transfer and to be ready for test
    {
      // Test
      timer.start();
      for (int j = 0; j < 10; j++) {
        servo_angle = random(0, 180);  // Pick random angle
        my_servo.write(servo_angle);
        random_angles[j] = servo_angle;  // Save angle
        random_delay[j] = pause_time;    // Save delay
        delay(pause_time);
      }
      total_time = timer.read();
      timer.stop();
      digitalWrite(servo_test_ready, LOW);        // Sending to Encoder Arduino that test is finished
      digitalWrite(servo_data_ready, HIGH);       // Sending to Encoder Arduino that it is ready for data transfer
      if (readEncoder_data && !readEncoder_test)  // Waiting Encoder Arduino to say it is ready for data transfer
      {
        // Data transfer
        Serial.print("All random test: ");
        Serial.print(test_no);
        Serial.print(".");
        Serial.println(i);
        for (int i = 0; i < 10; i++) {
          Serial.print("Test random angle_");
          Serial.print(i);
          Serial.print(": ");
          Serial.println(random_angles[i]);
        }
        Serial.print("Test constant delay");
        Serial.println(pause_time);
        Serial.print("Total time: ");
        Serial.println(total_time);
        my_servo.write(0);
        delay(1000);
        digitalWrite(servo_data_ready, LOW);  // Sending to Encoder Arduino that data transfer is finished
      }
    }
  }
}
