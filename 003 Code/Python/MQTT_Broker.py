import datetime
import firebase_admin
import paho.mqtt.client as mqtt

from firebase_admin import db
from firebase_admin import credentials


# 타임 스탬프 구하기
def get_timestamp():
	dt = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
	return dt

# MQTT 브로커 연결 상태 및 구독하기
def on_connect(client, userdata, flags, reason_code, properties):
	print(f"연결 상태: {reason_code}")
	
    # sensor의 하위에 있는 모든 topic 구독, QoS 설정 Level 1
	client.subscribe("sensor/+", 1)

# 구독한 topic의 메시지 받기
def on_message(client, userdata, msg):
	payload = float(msg.payload.decode())

	ref = db.reference('시설/' + msg.topic)
	ref.update({ get_timestamp(): payload })

cred = credentials.Certificate('C:/Users/Desktop/Downloads/capstone/capstone-c4974-firebase-adminsdk-c3yog-d6fde0f263.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://capstone-c4974-default-rtdb.firebaseio.com/'
})

mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

mqtt_client.connect("127.0.0.1", 1883, 60)

mqtt_client.loop_forever()