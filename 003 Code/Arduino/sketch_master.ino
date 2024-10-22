#include <SoftwareSerial.h>

#define DE_PIN 4
#define RE_PIN 5
#define RELAY_PIN1 7 // 조명 릴레이 핀 번호
#define RELAY_PIN2 8 // 급수 모터 릴레이 핀 번호

SoftwareSerial rs485(10, 11);  // rs485 RX = 10, TX = 11

// slave1 = 온/습도, 토양습도, 조도, 유량  slave2 = 모터 전류량/동작 제어

float temp_in, hum_in, temp_out, hum_out, flowRate;
int lightIntensity, soilMoisture;
float motor1Current, motor2Current;
String Shutter = "";

void setup() {
  pinMode(DE_PIN, OUTPUT);
  pinMode(RE_PIN, OUTPUT);
  pinMode(RELAY_PIN1, OUTPUT);
  pinMode(RELAY_PIN2, OUTPUT);
  digitalWrite(DE_PIN, LOW);
  digitalWrite(RE_PIN, LOW);
  digitalWrite(RELAY_PIN1, LOW);
  digitalWrite(RELAY_PIN2, LOW);

  rs485.begin(9600);
  Serial.begin(9600);
}

void loop() {
  control();
  delay(330);
  
  requestSlave1Data();
  delay(330);
  receiveData();

  requestSlave2Data();
  delay(330);
  receiveData();
}

void requestSlave1Data() {
  digitalWrite(DE_PIN, HIGH);
  rs485.print("REQUEST_SLAVE1\n");
  digitalWrite(DE_PIN, LOW);
}

void requestSlave2Data() {
  digitalWrite(DE_PIN, HIGH);
  rs485.print("REQUEST_SLAVE2\n");
  digitalWrite(DE_PIN, LOW);
}

void requestSlave2Control() {
  digitalWrite(DE_PIN, HIGH);
  rs485.print(Shutter);
  digitalWrite(DE_PIN, LOW);
}

void receiveData() {
  if (rs485.available()) {
    String receivedData = rs485.readStringUntil('\n');
    receivedData.trim();

    if (receivedData.startsWith("1")) { // 1번 슬레이브의 데이터 수집
      String sensorData = receivedData.substring(2);
      parseSlave1Data(sensorData);
    } else if (receivedData.startsWith("2")) { // 2번 슬레이브의 데이터 수집
      String currentData = receivedData.substring(2);
      parseSlave2Data(currentData);
    }
  }
}

// 1번 슬레이브 데이터 파싱 함수 (유량 데이터 추가)
void parseSlave1Data(String data) {
  int index;

  index = data.indexOf("TEMP_IN:");
  temp_in = data.substring(index + 8, data.indexOf(",", index)).toFloat();

  index = data.indexOf("HUM_IN:");
  hum_in = data.substring(index + 7, data.indexOf(",", index)).toFloat();

  index = data.indexOf("TEMP_OUT:");
  temp_out = data.substring(index + 9, data.indexOf(",", index)).toFloat();

  index = data.indexOf("HUM_OUT:");
  hum_out = data.substring(index + 8, data.indexOf(",", index)).toFloat();

  index = data.indexOf("LIGHT:");
  lightIntensity = data.substring(index + 6, data.indexOf(",", index)).toInt();

  index = data.indexOf("SOIL:");
  soilMoisture = data.substring(index + 5, data.indexOf(",", index)).toInt();

  index = data.indexOf("FLOW:");
  flowRate = data.substring(index + 5).toFloat();
}

// 2번 슬레이브 데이터 파싱 함수 (모터 전류량)
void parseSlave2Data(String data) {
  int index;

  index = data.indexOf("motor1Current:");
  motor1Current = data.substring(index + 14, data.indexOf("motor2Current:", index)).toFloat();

  index = data.indexOf("motor2Current:");
  motor2Current = data.substring(index + 14).toFloat();
}

// python 시리얼통신. 유량 데이터를 포함한 센서 데이터를 전송
void SerialCommu() {
  Serial.print(temp_in); // 내부온도
  Serial.print(",");
  Serial.print(hum_in); // 내부습도
  Serial.print(",");
  Serial.print(temp_out); // 외부온도
  Serial.print(",");
  Serial.print(hum_out); // 외부습도
  Serial.print(",");
  Serial.print(lightIntensity); // 조도
  Serial.print(",");
  Serial.print(soilMoisture); // 토양습도
  Serial.print(",");
  Serial.print(flowRate); // 유량
  Serial.print(",");
  Serial.print(motor1Current); // 모터1 전류
  Serial.print(",");
  Serial.println(motor2Current); // 모터2 전류
}

void control() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();

    // 모터 제어
    if (command == "SHUTTER_OPEN") {
      Shutter = "Shutter_Open";
      requestSlave2Control();
    }
    else if (command == "SHUTTER_CLOSE") {
      Shutter = "Shutter_Close";
      requestSlave2Control();
    }
    else if (command == "SHUTTER_STOP") {
      Shutter = "Stop";
      requestSlave2Control();
    }

    // 조명 제어
    if (command == "LIGHT_ON") {
      digitalWrite(RELAY_PIN1, HIGH);
    }
    if (command == "LIGHT_OFF") {
      digitalWrite(RELAY_PIN1, LOW);
    }

    // 급수모터 제어
    if (command == "SPRINKLER_ON"){
      digitalWrite(RELAY_PIN2, HIGH);
    }
    if (command == "SPRINKLER_OFF"){
      digitalWrite(RELAY_PIN2, LOW);
    }
  }
}