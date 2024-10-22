#include <SoftwareSerial.h>
#include <DHT.h>

#define DHTPIN_IN 2
#define DHTPIN_OUT 3
#define FLOW_SENSOR_PIN 6
#define DHTTYPE DHT22
#define SOIL_MOISTURE_PIN A0
#define LDR_PIN A1

#define DE_PIN 4
#define RE_PIN 5

int slaveID = 1;

DHT dht_in(DHTPIN_IN, DHTTYPE);
DHT dht_out(DHTPIN_OUT, DHTTYPE);

SoftwareSerial rs485(10, 11);  // rs485 RX = 10, TX = 11

volatile int flowPulseCount = 0;
float calibrationFactor = 7.5;  // YF-S401의 보정 계수
float flowRate = 0.0;  // 유량 값
unsigned long oldTime = 0;

void pulseCounter() {
  flowPulseCount++;
}

void setup() {
  pinMode(DE_PIN, OUTPUT);
  pinMode(RE_PIN, OUTPUT);
  digitalWrite(DE_PIN, LOW);
  digitalWrite(RE_PIN, LOW);

  pinMode(FLOW_SENSOR_PIN, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(FLOW_SENSOR_PIN), pulseCounter, FALLING);

  rs485.begin(9600);
  Serial.begin(9600);
  
  // DHT 센서 초기화
  dht_in.begin();
  dht_out.begin();

  oldTime = millis(); 
}

void loop() {
  if (rs485.available()) {
    String command = rs485.readStringUntil('\n');
    command.trim();

    if (command == "REQUEST_SLAVE1") {
      sendSensorData();
    }
  }

  if (millis() - oldTime > 1000) {
    calculateFlowRate();
    oldTime = millis();
  }
}

// 유량 계산 함수
void calculateFlowRate() {
  flowRate = ((1000.0 / (millis() - oldTime)) * flowPulseCount) / calibrationFactor;
  
  flowPulseCount = 0;
}

// 센서 데이터 전송 함수
void sendSensorData() {
  float temp_in = dht_in.readTemperature();
  float hum_in = dht_in.readHumidity();
  float temp_out = dht_out.readTemperature();
  float hum_out = dht_out.readHumidity();
  int soilMoisture = analogRead(SOIL_MOISTURE_PIN);
  int lightIntensity = analogRead(LDR_PIN);

  digitalWrite(DE_PIN, HIGH);
  digitalWrite(RE_PIN, HIGH);

  rs485.print(slaveID);
  rs485.print("TEMP_IN:"); rs485.print(temp_in);
  rs485.print(",HUM_IN:"); rs485.print(hum_in);
  rs485.print(",TEMP_OUT:"); rs485.print(temp_out);
  rs485.print(",HUM_OUT:"); rs485.print(hum_out);
  rs485.print(",LIGHT:"); rs485.print(lightIntensity);
  rs485.print(",SOIL:"); rs485.print(soilMoisture);
  rs485.print(",FLOW:"); rs485.print(flowRate);
  rs485.print("\n");

  digitalWrite(DE_PIN, LOW);
  digitalWrite(RE_PIN, LOW);
}