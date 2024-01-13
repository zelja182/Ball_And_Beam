#include <Servo.h>
#include "Timer.h"

int test_angles_1[4] = {30, 45, 60, 90};
int test_angles_2[6] = {-60, -45, -30, 30, 45, 60};
int start_0 = 0;
int start_90 = 90;
unsigned int time_var = 0;

int i=0;
int j=0; 

Servo my_servo;
Timer my_timer(MICROS);

void test_1()
{
  // Print Number of Test
  Serial.print("Test_1 no. ");
  Serial.print(i+1);
  Serial.print(".");
  Serial.print(j);
  Serial.println(" ");
  // Print Test Angle 
  Serial.print("Test angle: ");
  Serial.println(test_angles_1[i]);
  // Execute Test
  my_timer.start();
  my_servo.write(test_angles_1[i]); 
  delay(2000);
  time_var = my_timer.read();
  my_servo.write(start_0);
  delay(1500);

   // Print Execution Time
  Serial.print("Execution time: ");
  Serial.println(time_var);
  my_timer.stop();

  // Handle Counters 
  j++;
  if(j>=1)
  {
    i++; 
    j = 0;
  }

  if(i>=4)
  {
    Serial.println("The end of test");
  }
}

void test_2()
{
  int angle;
  angle = start_90 + test_angles_2[i];
  // Print Number of Test
  Serial.print("Test_2 no. ");
  Serial.print(i+1);
  Serial.print(".");
  Serial.print(j);
  Serial.println(" ");
  // Print Test Angle 
  Serial.print("Test angle: ");
  Serial.println(test_angles_2[i]);
  // Execute Test
  my_timer.start();
  my_servo.write(angle);
  delay(2000);
  time_var = my_timer.read();
  my_servo.write(start_90);
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
  
  if(i>=6)
  {
    Serial.println("The end of test");
  }

}

void test_3()
{
  int random_angles[6];
  int random_delay[6];
  // Print Number of Test
  Serial.print("Test_3 no. ");
  Serial.print(i+1);
  Serial.println(" ");

  for(j=0;j<6;j++)
  {
    random_angles[j] = start_90 + random(-45, 45);
    random_delay[j] = random(0, 1000);
  }

  // Execute Test
  my_timer.start();
  for(j=0;j<6;j++)
  {
    my_servo.write(random_angles[j]);
    delay(random_delay[j]);
  }
  my_servo.write(start_90);
  delay(500);
  time_var = my_timer.read();

  // Print Execution Time, Angles and Delays
  for(j=0;j<6;j++)
  {
    Serial.print("Angle_");
    Serial.print(j);
    Serial.print(": ");
    Serial.println(random_angles[j]);
    Serial.print("Delay_");
    Serial.print(j);
    Serial.print(": ");
    Serial.println(random_delay[j]);
  }
  Serial.print("Execution_time: ");
  Serial.println(time_var);
  my_timer.stop();
  
  // Handle Counters 
  i++;
}
void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  pinMode(2, INPUT_PULLUP);
  pinMode(5, OUTPUT);
  my_servo.attach(7, 580, 2420);
  my_servo.write(start_0);
  // attachInterrupt(digitalPinToInterrupt(2), test_1, FALLING);
}

void loop() {
  // put your main code here, to run repeatedly:
  if(digitalRead(2))
  {
    digitalWrite(5, HIGH);
  }
  else
  {
    delay(1500);
    digitalWrite(5, LOW);
    test_1();
  }
}
