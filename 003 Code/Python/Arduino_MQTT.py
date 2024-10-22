import time
import serial
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import threading
import queue

# 시리얼 포트 설정
ser = serial.Serial('COM5', 115200)
time.sleep(1)

# MQTT 브로커 설정
MQTT_BROKER = "127.0.0.1"
MQTT_TOPIC_INTEMP = "sensor/Intemp"
MQTT_TOPIC_OUTTEMP = "sensor/Outtemp"
MQTT_TOPIC_INHUMI = "sensor/Inhumi"
MQTT_TOPIC_OUTHUMI = "sensor/Outhumi"
MQTT_TOPIC_FLOW = "sensor/flow"
MQTT_TOPIC_LIGHT = "sensor/light"
MQTT_TOPIC_HIGH = "sensor/high"
MQTT_TOPIC_SOIL = "sensor/soil"
MQTT_TOPIC_CONTROL = "Control"

# 큐 생성
data_queue = queue.Queue()

def read_serial():
    try:
        while True:
            if ser.in_waiting > 0:
                data = ser.readline().decode('utf-8').strip()
                data_list = data.split(',')
                print(data)

                # 부족한 데이터는 기본값(0.0)으로 설정
                if len(data_list) < 7:
                    data_list.extend(['0.0'] * (8 - len(data_list)))
                data_queue.put(data_list)
    except Exception as e:
        print(f"Serial reading error: {e}")
    finally:
        ser.close()

def publish_mqtt():
    try:
        while True:
            if not data_queue.empty():
                data_list = data_queue.get()
                try:
                    Intemperature,Inhumidity,Outtemperature,Outhumidity,light,soil,flow_rate = map(float, data_list)
                    
                    # MQTT 메시지 퍼블리시
                    publish.single(MQTT_TOPIC_INTEMP, Intemperature, hostname=MQTT_BROKER)
                    publish.single(MQTT_TOPIC_INHUMI, Inhumidity, hostname=MQTT_BROKER)
                    publish.single(MQTT_TOPIC_OUTTEMP, Outtemperature, hostname=MQTT_BROKER)
                    publish.single(MQTT_TOPIC_OUTHUMI, Outhumidity, hostname=MQTT_BROKER)
                    publish.single(MQTT_TOPIC_LIGHT, light, hostname=MQTT_BROKER)
                    publish.single(MQTT_TOPIC_SOIL, soil, hostname=MQTT_BROKER)
                    publish.single(MQTT_TOPIC_FLOW, flow_rate, hostname=MQTT_BROKER)
                    
                except ValueError as e:
                    print(f"Data conversion error: {e}")
    except Exception as e:
        print(f"MQTT publishing error: {e}")

def on_connect(client, userdata, flags, reason_code, properties=None):
    print(f"Connected with result code {reason_code}")
    client.subscribe(MQTT_TOPIC_CONTROL, 1)

#Unity에서 받은 명령
def on_message(client, userdata, msg):
    print(f"Message received: Topic={msg.topic}, Payload={msg.payload.decode()}")
    if msg.payload.decode() == "LightOn":
        ser.write(b"LIGHT_ON\n")
    elif msg.payload.decode() == "LightOff":
        ser.write(b"LIGHT_OFF\n")
    if msg.payload.decode() == "ShutterOpen":
        ser.write(b"SHUTTER_OPEN\n")
    elif msg.payload.decode() == "ShutterClose":
        ser.write(b"SHUTTER_CLOSE\n")
    elif msg.payload.decode() == "ShutterStop":
        ser.write(b"SHUTTER_STOP\n")
    if msg.payload.decode() == "SprinklerOn":
        ser.wirte(b"SPRINKLER_ON\n")
    elif msg.payload.decod() == "SprinklerOff":
        ser.wirte(b"SPRINKLER_OFF\n")

def mqtt_subscribe():
    mqttc = mqtt.Client(protocol=mqtt.MQTTv311)
    mqttc.on_connect = on_connect
    mqttc.on_message = on_message

    mqttc.connect(MQTT_BROKER, 1883, 60)
    mqttc.loop_forever()

serial_thread = threading.Thread(target=read_serial)
mqtt_publish_thread = threading.Thread(target=publish_mqtt)
mqtt_subscribe_thread = threading.Thread(target=mqtt_subscribe)

serial_thread.start()
mqtt_publish_thread.start()
mqtt_subscribe_thread.start()
