#include <Servo.h>

// PID controller parameters
float Kp = 2.0; // Proportional gain
float Ki = 1.0; // Integral gain
float Kd = 0.5; // Derivative gain
float N = 10.0; // Filter coefficient for derivative

float dt = 0.01; // Time step (10 ms)
float integral = 0; // Integral sum
float prev_error = 0; // Previous error for derivative calculation
float prev_derivative = 0; // For filtering the derivative

float control_output = 0; // PID control output

// Setpoint and feedback
int setpoint = 25; // Desired distance in cm
float feedback = 0; // Measured distance from ultrasonic sensor
 
int angle_0 = 88;
bool systemActive = false;
Servo myServo;

void setup() {
  Serial.begin(115200); // Set baud rate to 115200 for faster data transmission

  // Initialize servo motor
  myServo.attach(9, 580, 2420);

  // Initialize ultrasonic sensor pins
  pinMode(5, OUTPUT);  // Triger Pin
  pinMode(6, INPUT);  // Eho pin 

  // Set initial servo position to neutral (90 degrees or center of the range)
  myServo.write(88);
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read(); // Read the incoming byte

    if (command == 'S') {
      systemActive = false; // Stop the system
      myServo.write(88); // Optionally, set servo to neutral position
      Serial.println("System stopped");
    }
    else if (command == 'G') {
      systemActive = true; // Start the system
      Serial.println("System running");
    }
  }

  if (systemActive) {
    // Measure distance using blocking ultrasonic sensor
    float distance = getUltrasonicDistanceBlocking();
    
    // If a valid distance is returned, update feedback
    if (distance != -1) {
      feedback = distance;
    }

    // Compute error
    float error = setpoint - feedback;

    // Proportional term
    float P = Kp * error;

    // Integral term
    integral += error * dt;
    float I = Ki * integral;

    // Derivative term with filter
    float derivative = (error - prev_error) / dt;
    float filtered_derivative = (N * derivative + prev_derivative) / (1 + N * dt);
    float D = Kd * filtered_derivative;

    // PID output
    control_output = P + I + D;

    // Constrain output to the range of -30 to 30 degrees
    control_output = constrain(control_output, -30.0, 30.0);
    control_output += angle_0;

    // Map the control output to the servo's PWM range
    int pwmValue = map(control_output, 0, 180, 580, 2420);

    // Send the PWM signal to the servo motor
    myServo.writeMicroseconds(pwmValue);

    // Update previous values for the next loop
    prev_error = error;
    prev_derivative = filtered_derivative;

    // Send only the distance value over serial communication
    unsigned long currentTime = millis(); // Get the elapsed time in milliseconds
    Serial.print(currentTime);
    Serial.print(feedback);
  }

  // Wait for the next loop iteration (10 ms)
  delay(dt * 1000);
}

// Function for blocking ultrasonic distance measurement
float getUltrasonicDistanceBlocking() {
  // Send a 10µs pulse to trigger the sensor
  digitalWrite(5, LOW);
  delayMicroseconds(2);
  digitalWrite(5, HIGH);
  delayMicroseconds(10);
  digitalWrite(5, LOW);

  // Measure pulse duration
  long duration = pulseIn(6, HIGH);

  // Calculate distance in centimeters
  float distance = (duration / 2.0) * 0.0344 + 2; // Speed of sound is 0.0344 cm/µs; radius of ping pong ball 2cm 

  // Return distance
  return distance;
}
