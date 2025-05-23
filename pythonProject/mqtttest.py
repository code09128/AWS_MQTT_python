import time
import paho.mqtt.client as mqtt
import ssl
import logging

# 設置日誌
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# MQTT broker 配置
broker = "a2vbveng9jsgb1-ats.iot.ap-northeast-1.amazonaws.com"
port = 8883
topic = "house/bulb1"

# SSL 憑證路徑
caPath = "D:/Dustin/awskey/mqtt/AmazonRootCA1.pem"
certPath = "D:/Dustin/awskey/mqtt/ea6df150093d53d95f3c19bb586b33c31f7759b98e63b414ca67460530c27c76-certificate.pem.crt"
keyPath = "D:/Dustin/awskey/mqtt/ea6df150093d53d95f3c19bb586b33c31f7759b98e63b414ca67460530c27c76-private.pem.key"

# 當連接成功時的回調
def on_connect(client, userdata, flags, rc):
    rc_codes = {
        0: "連接成功",
        1: "協議版本錯誤",
        2: "無效的客戶端標識",
        3: "伺服器無法使用",
        4: "錯誤的用戶名或密碼",
        5: "未授權"
    }
    logger.info(f"連接狀態: {rc_codes.get(rc, f'未知錯誤 {rc}')}")
    if rc == 0:
        client.subscribe(topic)
        logger.info(f"已訂閱主題: {topic}")

# 當收到訊息時的回調
def on_message(client, userdata, msg):
    logger.info(f"收到訊息 {msg.topic}: {msg.payload.decode()}")

# 斷開連接的回調
def on_disconnect(client, userdata, rc):
    logger.info("已斷開連接")

try:
    # 建立客戶端
    client = mqtt.Client(protocol=mqtt.MQTTv5)

    # 設置回調函數
    client.on_connect = on_connect
    client.on_message = on_message
    
    # 設置 SSL/TLS
    client.tls_set(
        ca_certs=caPath,
        certfile=certPath,
        keyfile=keyPath,
        cert_reqs=ssl.CERT_REQUIRED,
        tls_version=ssl.PROTOCOL_TLSv1_2
    )

    # 連接到 broker
    logger.info(f"正在連接到 broker {broker}...")
    client.connect(broker, port, keepalive=60)

    # 發布訊息
    logger.info("發布測試訊息...")
    client.publish(topic, "python test mqttHello World!", qos=1)

    # 保持連接
    logger.info("開始運行...")
    client.loop_forever()

except FileNotFoundError as e:
    logger.error(f"找不到憑證文件: {e}")
except ssl.SSLError as e:
    logger.error(f"SSL 錯誤: {e}")
except ConnectionRefusedError as e:
    logger.error(f"連接被拒絕: {e}")
except KeyboardInterrupt:
    logger.info("程式被使用者中斷")
except Exception as e:
    logger.error(f"發生錯誤: {e}", exc_info=True)
finally:
    if 'client' in locals():
        client.disconnect()
        logger.info("已清理連接")