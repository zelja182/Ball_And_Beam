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

// First-order filter on the ball velocity only. The P and I terms still see the
// raw measurement, so this removes the noise the D term differentiates without
// delaying the rest of the loop.
const float D_TAU_S = 0.10f;

// Paste from MATLAB after tuning
float Kp = -1.2f;
float Ki = -0.01f;
float Kd = -0.7f;

bool running = false;
float distance_mm = 0.0f;
float beam_deg = 0.0f;
float integral = 0.0f;
float prev_error = 0.0f;
float d_filt = 0.0f;
bool sample_ready = false;
unsigned long t0_ms = 0;
unsigned long next_tick_ms = 0;

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
    sample_ready = true;
  }
}

float pidStep(float error) {
  if (fabs(error) <= TOLERANCE_MM) {
    integral = 0.0f;
    prev_error = 0.0f;
    d_filt = 0.0f;
    beam_deg = 0.0f;
    return beam_deg;
  }

  const float dt = LOOP_MS / 1000.0f;

  integral += error * dt;

  float d_raw = (error - prev_error) / dt;
  d_filt += (dt / (D_TAU_S + dt)) * (d_raw - d_filt);
  prev_error = error;

  beam_deg = constrain(Kp * error + Ki * integral + Kd * d_filt, BEAM_MIN, BEAM_MAX);
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

  beamServo.attach(SERVO_PIN);
  holdNeutral();

  if (!lox.begin()) {
    Serial.println(F("VL53L0X init failed"));
    while (1) {
      delay(100);
    }
  }

  lox.startRangeContinuous();

  Serial.println(F("Ball and Beam v2 (D-filter)"));
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
      next_tick_ms = t0_ms + LOOP_MS;
      integral = 0.0f;
      prev_error = 0.0f;
      d_filt = 0.0f;
      sample_ready = false;
      holdNeutral();
      Serial.println(F("RUN"));
    } else if (cmd == 'S' || cmd == 's') {
      running = false;
      holdNeutral();
      Serial.println(F("STOP"));
    }
  }

  // Poll the sensor as often as possible; the call returns immediately when no
  // new range is ready.
  readDistance();

  if (!running) {
    return;
  }

  if ((long)(millis() - next_tick_ms) < 0) {
    return;
  }
  next_tick_ms += LOOP_MS;
  if ((long)(millis() - next_tick_ms) > (long)LOOP_MS) {
    next_tick_ms = millis() + LOOP_MS;
  }

  // Without a fresh measurement the derivative would read zero and then double
  // on the next sample, so the command is held instead of recomputed.
  if (sample_ready) {
    sample_ready = false;
    float error = SETPOINT_MM - distance_mm;
    setBeamAngle(pidStep(error));
  }

  logData();
}
