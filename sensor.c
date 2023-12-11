#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/msg.h>
#include <string.h>
#include <time.h>

#define MESSAGE_QUEUE_KEY 1234

// 센서 데이터를 담는 구조체 정의
struct sensor_data
{
    long mtype;
    int temperature;
    float humidity;
};

int main()
{
    srand(time(NULL));

    int msqid;
    key_t key;
    int rc;
    struct sensor_data sd;

    key = MESSAGE_QUEUE_KEY;
    if ((msqid = msgget(key, 0666 | IPC_CREAT)) < 0)
    {
        perror("msgget()");
        return -1;
    }

    while (1)
    {
        // 센서 데이터 생성
        int temperature = rand() % 30;                   // 온도
        float humidity = (float)rand() / RAND_MAX * 100; // 습도

        // 센서 데이터 구조체 값 입력
        sd.mtype = 1;
        sd.temperature = temperature;
        sd.humidity = humidity;

        rc = msgsnd(msqid, &sd, sizeof(struct sensor_data) - sizeof(long), 0);
        if (rc == -1)
        {
            perror("msgsnd()");
            return -1;
        }

        printf("Message sent: temperature: %d     humidity: %.2f\n", sd.temperature, sd.humidity);
        fflush(stdout);
        sleep(3);
    }

    return 0;
}