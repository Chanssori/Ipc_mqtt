# Ipc_mqtt

## 프로젝트: 온습도 제어 시스템

온습도 제어 시스템은 IPC(Inter-Process Communication), MySQL 데이터베이스, MQTT를 결합하여 센서 데이터를 효율적으로 관리합니다.

프로젝트에는 `Sensor.c`, `Consumer.c`, `Database_mysql.py`, `mqtt_sub.py` 네 개의 주요 파일이 포함되어 있습니다.

### 작동 방식
**Sensor – IPC – DB & MQTT_Publish – MQTT_Subscribe**

#### Sensor - IPC
- **Sensor.c:** 무작위 온도 (0-30) 및 습도 (0-1) 데이터를 생성합니다.
- **Sensor.c:** 센서 데이터를 메시지 대기열로 보냅니다.
- **Consumer.c:** IPC에 대한 메시지 대기열을 활용합니다.
- **Consumer.c:** 메시지 큐에서 데이터를 수신하고 출력합니다.

#### Sensor - DB & MQTT_Publish
- **Sensor.c:** 센서 데이터를 메시지 큐에 전송합니다.
- **Database_mysql.py:** 데이터를 수신하고, MySQL DB에 삽입하며, MQTT Topic에 발행합니다.

#### DB & MQTT_Publish – MQTT_Subscribe
- **Database_mysql.py (Mqtt_Publish):** 데이터를 JSON 형식으로 변환하고 MQTT Topic에 Publish합니다.
- **Mqtt_sub.py:** Topic을 Subscribe하고 `on_message` 콜백 함수를 정의합니다.

### 실행 순서
```bash
gcc sensor.c -o sensor
./sensor

gcc consumer.c -o consumer -lrt
./consumer

python3 database_mysql.py

python3 mqtt_sub.py
```

### MYSQL에서 데이터 확인
```mysql
SELECT * FROM SENSOR_DATA;
```
