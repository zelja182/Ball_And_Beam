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
const unsigned long LOOP_MS = 50;

// First-order low-pass on the distance reading. The D term differentiates
// sensor noise, so a larger tau means a calmer servo but more phase lag.
const float FILTER_TAU_S = 0.12f;

// Paste from MATLAB after tuning
float Kp = -2.0f;
float Ki = -0.09f;
float Kd = -1.5f;

bool running = false;
float distance_mm = 0.0f;
float distance_filt_mm = 0.0f;
bool filter_ready = false;
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
  if (raw == 65535) {
    return;
  }

  distance_mm = (float)raw;

  if (!filter_ready) {
    distance_filt_mm = distance_mm;
    filter_ready = true;
    return;
  }

  const float dt = LOOP_MS / 1000.0f;
  const float alpha = dt / (FILTER_TAU_S + dt);
  distance_filt_mm += alpha * (distance_mm - distance_filt_mm);
}

float pidStep(float error) {
  const float dt = LOOP_MS / 1000.0f;

  float D = Kd * (error - prev_error) / dt;
  prev_error = error;

  float u = Kp * error + Ki * integral + D;

  // Anti-windup by conditional integration: keep the integral frozen while the
  // command sits at a limit and the new contribution would push further out.
  float delta_i = Ki * error * dt;
  bool winding_up = (u >= BEAM_MAX && delta_i > 0.0f) ||
                    (u <= BEAM_MIN && delta_i < 0.0f);
  if (!winding_up) {
    integral += error * dt;
    u = Kp * error + Ki * integral + D;
  }

  beam_deg = constrain(u, BEAM_MIN, BEAM_MAX);
  return beam_deg;
}

void logData() {
  // Raw distance is logged so the filter can be reproduced offline.
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

  beamServo.attach(SERVO_PIN);
  holdNeutral();

  if (!lox.begin()) {
    Serial.println(F("VL53L0X init failed"));
    while (1) {
      delay(100);
    }
  }

  lox.startRangeContinuous();

  Serial.println(F("Ball and Beam v2 (LPF)"));
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
      filter_ready = false;
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

  float error = SETPOINT_MM - distance_filt_mm;
  setBeamAngle(pidStep(error));
  logData();

  delay(LOOP_MS);
}
