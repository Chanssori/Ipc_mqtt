# Ipc_mqtt

프로젝트: 온도 및 습도 조절 시스템

온습도 제어 시스템은 효율적인 데이터 교환을 위해 IPC(Inter-Process Communication), MySQL 데이터베이스, MQTT를 조합하여 센서 데이터를 관리합니다. 


프로젝트는 Sensor.c, Consumer.c, Database_mysql.py 및 mqtt_sub.py의 네 가지 주요 파일로 구성됩니다.

작동 방식
Sensor – IPC - DB & MQTT Publish - MQTT Subscriber

Sensor - IPC
Sensor.c: 임의의 온도(0-30) 및 습도(0-1) 데이터를 생성합니다.
Sensor.c는 센서 데이터를 메시지 대기열로 보냅니다.
Consumer.c: IPC용 메시지 대기열을 활용합니다.
Consumer.c는 메시지 큐로부터 메시지 대기열에서 데이터를 수신하고 출력합니다.


Sensor - DB & MQTT Publish
Sensor.c: 센서 데이터를 메시지 대기열로 보냅니다.
Database_mysql.py: 데이터를 수신하여 MySQL 데이터베이스에 삽입하고 MQTT topic에 publish합니다.


DB 및 MQTT_PUBLISH – MQTT_
Database_mysql.py (Mqtt_pub): 데이터를 JSON으로 변환하여 MQTT topic에 publish합니다.
Mqtt_sub.py: topic을 subscribe하고 on_message 콜백 함수를 정의합니다.


실행 순서
```linux bash
gcc sensor.c -o sensor
./sensor

gcc consumer.c -o consumer -lrt
./consumer

python3 database_mysql.py

python3 mqtt_sub.py
```

MYSQL에서 데이터 확인
```mysql
SELELCT * FROM SENSOR_DATA;
```


