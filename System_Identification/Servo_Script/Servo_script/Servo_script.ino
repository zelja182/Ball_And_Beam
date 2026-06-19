#include <Servo.h>
#include "Timer.h"

int test_angles[8] = {-45, -30, -20, -10, 10, 20, 30, 45};  
int zero_pwm = map(0, -135, 135, 500, 2500);
unsigned int time_var = 0;

int i=0;
int j=0; 

Servo my_servo;
Timer my_timer(MICROS);


void test_1()
{
  if(i==8)
  {
    Serial.println("The end of test");
    i++;
  }
  else if (i<8)
  {
    int angle;
    int pwm = map(test_angles[i], -135, 135, 500, 2500);
    // Print Number of Test
    Serial.print("Test_1 no. ");
    Serial.print(i+1);
    Serial.print(".");
    Serial.print(j);
    Serial.println(" ");
    // Print Test Angle 
    Serial.print("Test angle: ");
    Serial.println(test_angles[i]);
    Serial.print("Test pwm: ");
    Serial.println(pwm);
    // Execute Test
    my_timer.start();
    my_servo.writeMicroseconds(pwm);
    delay(2000);
    time_var = my_timer.read();
    my_servo.writeMicroseconds(zero_pwm);
    delay(1500);
    
    // Print Execution Time
    Serial.print("Execution time: ");
    Serial.println(time_var);
    my_timer.stop();

    // Handle Counters 
    j++;
    if(j>=5)
    {
      i++; 
      j = 0;
    }
  }
}

void test_2()
{
  if(i==15)
  {
    Serial.println("The end of test");
    i++;
  }
  else if (i<15)
  {
    int random_angles[6];
    int random_pwms[6];
    int random_delay[6];
    // Print Number of Test
   
    // Generate data for test
    for(j=0;j<6;j++)
    {
      random_angles[j] = random(-45, 45);  // Test data 2-1
      // random_angles[j] = random(-30, 30);  // Test data 2-2
      random_pwms[j] = map(random_angles[j], -135, 135, 500, 2500);  
      random_delay[j] = random(10, 100) * 10;
    }

    // Execute Test
    my_timer.start();
    for(j=0;j<6;j++)
    {
      my_servo.writeMicroseconds(random_pwms[j]);
      delay(random_delay[j]);
    }
    my_servo.writeMicroseconds(zero_pwm);
    delay(500);
    time_var = my_timer.read();

    Serial.print("Test_2 no. ");
    Serial.print(i+1);
    Serial.println(" ");

    // Print Execution Time, Angles and Delays
    for(j=0;j<6;j++)
    {
      Serial.print("angle");
      Serial.print(": ");
      Serial.println(random_angles[j]);
      Serial.print("delay");
      Serial.print(": ");
      Serial.println(random_delay[j]);
    }
    Serial.print("Execution_time: ");
    Serial.println(time_var);
    my_timer.stop();
    
    // Handle Counters 
    i++;
  }
}


void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  pinMode(2, INPUT_PULLUP);  // Button Pin
  pinMode(7, OUTPUT);        // LED Pin
  my_servo.attach(5);        // Servo Pin

  my_servo.writeMicroseconds(zero_pwm); 
  Serial.print("Zero pwm: ");
  Serial.println(zero_pwm);
  // attachInterrupt(digitalPinToInterrupt(2), test_1, FALLING);
}

void loop() {
  // put your main code here, to run repeatedly:
  if(digitalRead(2))
  {
    digitalWrite(7, HIGH);
  }
  else
  {
    delay(1500);
    digitalWrite(7, LOW);
    test_2();
  }
}
