#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/msg.h>

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
    int msqid;
    key_t key;
    int rc;
    struct sensor_data sd;

    key = MESSAGE_QUEUE_KEY;
    if ((msqid = msgget(key, IPC_CREAT | 0666)) < 0)
    {
        perror("msgget()");
        return -1;
    }

    while (1)
    {
        rc = msgrcv(msqid, &sd, sizeof(struct sensor_data) - sizeof(long), 1, 0);
        if (rc == -1)
        {
            perror("msgrcv()");
            return -1;
        }

        printf("Received: temperature: %d     humidity: %.2f\n", sd.temperature, sd.humidity);
        fflush(stdout);

        sleep(3);
    }

    return 0;
}