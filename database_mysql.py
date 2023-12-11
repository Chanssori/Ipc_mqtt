import pymysql
import paho.mqtt.client as mqtt
import json
import time
import sysv_ipc
import struct


def insert_sensor_data(temperature, humidity):
    # MySQL 서버에 연결
    connection = pymysql.connect(
        host="127.0.0.1",
        user="root",
        password="1234",
        database="test",
        cursorclass=pymysql.cursors.DictCursor
    )

    try:
        # 데이터베이스와 상호 작용하기 위한 커서 객체 생성
        with connection.cursor() as cursor:
            # 테이블이 없으면 생성
            create_table_query = """
            CREATE TABLE IF NOT EXISTS sensor_data (
                id INT AUTO_INCREMENT PRIMARY KEY,
                temperature INT,
                humidity FLOAT
            )
            """
            cursor.execute(create_table_query)
            connection.commit()

            # 센서 데이터 삽입
            insert_query = """
            INSERT INTO sensor_data (temperature, humidity)
            VALUES (%s, %s)
            """
            cursor.execute(insert_query, (temperature, humidity))
            connection.commit()

    finally:
        # 연결 종료
        connection.close()


def send(client, temperature, humidity):
    sensor_data = {"temperature": temperature, "humidity": humidity}

    # 딕셔너리를 JSON 형식의 문자열로 변환
    payload = json.dumps(sensor_data)

    # MQTT 토픽에 센서 데이터 전송
    client.publish("sensor_data_topic", payload)

    print(f"Sent: temperature={temperature}, humidity={humidity}")


def receive_sensor_data(client):
    # 메시지 큐에 연결
    msqid = 1234  # sensor.c에서 정의한 키와 동일
    mq = sysv_ipc.MessageQueue(msqid)

    while True:
        message, msg_type = mq.receive()
        temperature, humidity = struct.unpack("=if", message)
        print(f"Received: temperature={temperature}, humidity={humidity}")

        # MySQL에 센서 데이터 삽입
        insert_sensor_data(temperature, humidity)

        # MQTT로 센서 데이터 전송
        send(client, temperature, humidity)
        time.sleep(3)


if __name__ == "__main__":

    client = mqtt.Client()
    client.connect("127.0.0.1", 1883, 60)

    # Start the MQTT loop in the background
    client.loop_start()

    while True:
        receive_sensor_data(client)
        time.sleep(3)
