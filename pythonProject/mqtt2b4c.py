import time
import paho.mqtt.client as mqtt
import json

BROKER = "mqtt.onusflux.com"
PORT = 18830
TOPIC1 = "mqttlei/2bawc"
TOPIC2 = "mqttlei/4bawc"
USERNAME = "mqttlei"
PASSWORD = "leader1970"

def publish():
    data = {
        "sensor": "temperature",
        "value": 22.5,
        "unit": "C"
    }
    json_data = json.dumps(data)
    client.publish(TOPIC1, json_data)
    print(f"已發送訊息: {json_data}")

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(TOPIC1)
    client.subscribe(TOPIC2)

def on_message(client, userdata, msg):
    print(f"Received message on {msg.topic}: {msg.payload.decode()}")

# 基本client連線設定
client = mqtt.Client()
client.username_pw_set(USERNAME, PASSWORD)

client.on_connect = on_connect
client.on_message = on_message

try:
    client.connect(BROKER, PORT, 60)
    print("Connecting to broker...")

    client.loop_start()  # 啟動背景接收 thread

    while True:
        publish()
        time.sleep(5)  # 每 5 秒發送一次

except Exception as e:
    print(f"Connection failed: {e}")

except KeyboardInterrupt:
    print("中斷執行，關閉連線")
    client.loop_stop()
    client.disconnect()
