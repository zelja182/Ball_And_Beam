#include <Servo.h>
#include "Adafruit_VL53L0X.h"

// ---------- Hardware ----------
const int SERVO_PIN = 5;
const int ZERO_PWM = map(0, -135, 135, 500, 2500);

const float BEAM_MIN = -45.0f;
const float BEAM_MAX =  45.0f;

Servo beamServo;
Adafruit_VL53L0X lox;

// ---------- Control ----------
const float SETPOINT_MM = 250.0f;
const float TOLERANCE_MM = 5.0f;
const unsigned long LOOP_MS = 50;

// Paste from MATLAB after tuning
float Kp = 1.0f;
float Ki = 0.0f;
float Kd = 0.0f;

bool running = false;
float distance_mm = 0.0f;
float beam_deg = 0.0f;
float integral = 0.0f;
float prev_error = 0.0f;
unsigned long t0_ms = 0;

void setBeamAngle(float angle_deg) {
  float pwm_f = 500.0f + (angle_deg + 135.0f) * (2000.0f / 270.0f);
  int pwm = (int)lround(pwm_f);
  beamServo.writeMicroseconds(pwm);
}

void holdNeutral() {
  beam_deg = 0.0f;
  beamServo.writeMicroseconds(ZERO_PWM);
}

void readDistance() {
  if (!lox.isRangeComplete()) {
    return;
  }

  uint16_t raw = lox.readRange();
  if (raw != 65535) {
    distance_mm = (float)raw;
  }
}

float pidStep(float error) {
  if (fabs(error) <= TOLERANCE_MM) {
    integral = 0.0f;
    prev_error = 0.0f;
    return 0.0f;
  }

  const float dt = LOOP_MS / 1000.0f;

  integral += error * dt;
  float D = Kd * (error - prev_error) / dt;
  prev_error = error;

  beam_deg = constrain(-(Kp * error + Ki * integral + D), BEAM_MIN, BEAM_MAX);
  return beam_deg;
}

void logData() {
  Serial.print(millis() - t0_ms);
  Serial.print(',');
  Serial.print((int)lround(distance_mm));
  Serial.print(',');
  Serial.println(beam_deg, 2);
}

void setup() {
  Serial.begin(115200);
  while (!Serial) {
    delay(1);
  }

  beamServo.attach(5);
  holdNeutral();

  if (!lox.begin()) {
    Serial.println(F("VL53L0X init failed"));
    while (1) {
      delay(100);
    }
  }

  lox.startRangeContinuous();

  Serial.println(F("Ball and Beam v1"));
  Serial.println(F("G = start, S = stop"));
  Serial.println(F("time_ms,distance_mm,beam_deg"));
}

void loop() {
  if (Serial.available()) {
    char cmd = Serial.read();
    while (Serial.available()) {
      Serial.read();
    }

    if (cmd == 'G' || cmd == 'g') {
      running = true;
      t0_ms = millis();
      integral = 0.0f;
      prev_error = 0.0f;
      holdNeutral();
      Serial.println(F("RUN"));
    } else if (cmd == 'S' || cmd == 's') {
      running = false;
      holdNeutral();
      Serial.println(F("STOP"));
    }
  }

  if (!running) {
    return;
  }

  readDistance();

  float error = SETPOINT_MM - distance_mm;
  setBeamAngle(pidStep(error));
  logData();

  delay(LOOP_MS);
}
