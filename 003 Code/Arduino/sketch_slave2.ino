#include <SoftwareSerial.h>

#define CURRENT_SENSOR1_PIN A0
#define CURRENT_SENSOR2_PIN A1
#define MOTOR1_IN1 6
#define MOTOR1_IN2 7
#define MOTOR1_EN 9
#define MOTOR2_IN1 8
#define MOTOR2_IN2 10
#define MOTOR2_EN 11

#define DE_PIN 4
#define RE_PIN 5

int slaveID = 2;

SoftwareSerial rs485(10, 11);  // RS485 통신 (RX = 10, TX = 11)

void setup() {
  pinMode(MOTOR1_IN1, OUTPUT);
  pinMode(MOTOR1_IN2, OUTPUT);
  pinMode(MOTOR1_EN, OUTPUT);
  
  pinMode(MOTOR2_IN1, OUTPUT);
  pinMode(MOTOR2_IN2, OUTPUT);
  pinMode(MOTOR2_EN, OUTPUT);

  pinMode(DE_PIN, OUTPUT);
  pinMode(RE_PIN, OUTPUT);
  digitalWrite(DE_PIN, LOW);
  digitalWrite(RE_PIN, LOW);

  rs485.begin(9600);
  Serial.begin(9600);
}

void loop() {
  if (rs485.available()) {
    String command = rs485.readStringUntil('\n');
    command.trim();

    if (command == "REQUEST_SLAVE2") {
      sendCurrentData();
    } else {
      controlMotors(command);
    }
  }
}

void controlMotors(String command) {
  if (command == "ShutterOpen") {
    digitalWrite(MOTOR1_IN1, HIGH);
    digitalWrite(MOTOR1_IN2, LOW);
    analogWrite(MOTOR1_EN, 255);

    digitalWrite(MOTOR2_IN1, LOW);
    digitalWrite(MOTOR2_IN2, HIGH);
    analogWrite(MOTOR2_EN, 255);
  }
  else if (command == "ShutterClose") {
    digitalWrite(MOTOR1_IN1, LOW);
    digitalWrite(MOTOR1_IN2, HIGH);
    analogWrite(MOTOR1_EN, 255);

    digitalWrite(MOTOR2_IN1, HIGH);
    digitalWrite(MOTOR2_IN2, LOW);
    analogWrite(MOTOR2_EN, 255);
  }
  else if (command == "Stop") {
    digitalWrite(MOTOR1_IN1, LOW);
    digitalWrite(MOTOR1_IN2, LOW);
    analogWrite(MOTOR1_EN, 0);

    digitalWrite(MOTOR2_IN1, LOW);
    digitalWrite(MOTOR2_IN2, LOW);
    analogWrite(MOTOR2_EN, 0);
  }
}

void sendCurrentData() {
  int sensor1Value = analogRead(CURRENT_SENSOR1_PIN);
  int sensor2Value = analogRead(CURRENT_SENSOR2_PIN);
  float motor1Current = sensor1Value * (5.0 / 1023.0);
  float motor2Current = sensor2Value * (5.0 / 1023.0);

  digitalWrite(DE_PIN, HIGH);
  digitalWrite(RE_PIN, HIGH);

  rs485.print(slaveID);
  rs485.print("motor1Current:");
  rs485.print(motor1Current);
  rs485.print("motor2Current:");
  rs485.print(motor2Current);
  rs485.print("\n");

  digitalWrite(DE_PIN, LOW);
  digitalWrite(RE_PIN, LOW);
}
