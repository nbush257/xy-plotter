#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include "utility/Adafruit_MS_PWMServoDriver.h"

Adafruit_MotorShield s = Adafruit_MotorShield();
Adafruit_StepperMotor *x = s.getStepper(400, 2);
Adafruit_StepperMotor *y = s.getStepper(400, 1);

//int x_target = 0;
//int y_target = 0;
int x_pos = 0;
int y_pos = 0;
char mode = 'D';
int sleep_time = 0;
int step_mode = SINGLE;

float x_delta;
float y_delta;

const int y_limit_pin = 4;
const int x_limit_pin = 3;

bool x_coarse = false;
bool y_coarse = false;
bool x_homed = false;
bool y_homed = false;

void setup() {
  // put your setup code here, to run once:
  pinMode(y_limit_pin, INPUT);
  pinMode(x_limit_pin, INPUT);
  Serial.begin(9600);
  delay(100);
  while (!Serial.available()) {} //wait for input
  Serial.write(0);
  s.begin();
  x->setSpeed(100);
  y->setSpeed(100);
  // ==============
  // Coarse homing
  // ==============
  while (!x_coarse) {
    x->step(1, BACKWARD, DOUBLE);
    if (digitalRead(x_limit_pin) == HIGH) {
      x_coarse = true;
    }
  }

  while (!y_coarse) {
    y->step(1, FORWARD, DOUBLE);
    if (digitalRead(y_limit_pin) == HIGH) {
      y_coarse = true;
    }
  }
// ==============
// Fine Homing
// ==============
// Give space
x->step(20,FORWARD, DOUBLE);
y->step(20,BACKWARD, DOUBLE);
// Home
  while (!x_homed) {
    x->step(1, BACKWARD, MICROSTEP);
    if (digitalRead(x_limit_pin) == HIGH) {
      x_homed = true;
    }
  }

  while (!y_homed) {
    y->step(1, FORWARD, MICROSTEP);
    if (digitalRead(y_limit_pin) == HIGH) {
      y_homed = true;
    }
  }
  Serial.write(1);
  Serial.flush();
  x->release();
  y->release();
  while (Serial.available()) {
    Serial.read(); //clear serial input
  }
}

void loop() {
  // ================================ //
  // Get X target
  // ================================ //
  while (!Serial.available()) {} //wait for input
  int x_target = Serial.parseInt();
  // Prevent stupid inputs
  if (x_target > 390) {
    x_target = 390;
  }
  if (x_target < 0) {
    x_target = 0;
  }
  // Let python know the message was received
  Serial.write(1);

  // ================================ //
  // Get Y target
  // ================================ //
  while (!Serial.available()) {} //wait for input

  int y_target = Serial.parseInt();
  // Prevent stupid inputs
  if (y_target > 325) {
    y_target = 325;
  }
  if (y_target < 0) {
    y_target = 0;
  }
  
  // Let python know the message was received
  Serial.write(1);
  // ================================ //
  // Get mode ('S','D','M','I')
  // ================================ //
  while (!Serial.available()) {} //wait for input
  char mode = Serial.read();
  // Let python know the message was received
  Serial.write(1);
  
  // ================================ //
  // Calculate Delta
  // ================================ //
  x_delta = (x_target - x_pos) * 5.55556;
  y_delta = (y_target - y_pos) * 5.55556;

  // Wrie message of new coordinates
  Serial.println("X target:");
  Serial.println(x_target, DEC);

  Serial.println("Y target:");
  Serial.println(y_target, DEC);


  // ================================ //
  // Set step_mode
  // ================================ //

  if (mode == 'S') {
    step_mode = SINGLE;
  }
  else if (mode == 'D') {
    step_mode = DOUBLE;
  }
  else if (mode == 'I') {
    step_mode = INTERLEAVE;
  }
  else if (mode == 'M') {
    step_mode = MICROSTEP;
  }

  // ================================ //
  // Move X
  // ================================ //

  if (x_delta >= 0) {
    x->step(x_delta, FORWARD, step_mode);
  }
  else {
    x_delta = -x_delta;
    x->step(x_delta, BACKWARD, step_mode);
  }

  // ================================ //
  // Move Y
  // ================================ //
  if (y_delta >= 0) {
    y->step(y_delta, BACKWARD, step_mode);
  }
  else {
    y_delta = -y_delta;
    y->step(y_delta, FORWARD, step_mode);
  }
  // ================================ //
  // Set new position
  // ================================ //
  x_pos = x_target;
  y_pos = y_target;

  // Let python know the motors have finished moving
  Serial.write(2);

  x->release();
  y->release();
}

