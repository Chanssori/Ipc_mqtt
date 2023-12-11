import paho.mqtt.client as mqtt
import json
import time


def on_message(client, userdata, msg):
    # 수신된 메시지의 페이로드를 디코딩하고 JSON 파싱
    payload = msg.payload.decode()
    data = json.loads(payload)

    temperature = data.get("temperature")
    humidity = data.get("humidity")
    print(f"Received: Temperature={temperature}, Humidity={humidity}")


if __name__ == "__main__":
    client = mqtt.Client()
    client.connect("127.0.0.1", 1883, 60)

    # MQTT 토픽 구독 설정
    client.subscribe("sensor_data_topic")

    # 메시지 수신 이벤트에 대한 콜백 함수 설정
    client.on_message = on_message

    client.loop_start()

    while True:
        time.sleep(3)
