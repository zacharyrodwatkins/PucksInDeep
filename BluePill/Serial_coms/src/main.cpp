#include <pi_coms.h>

char send[SEND_SIZE];  // 4 floats, 16 bytes
byte received[REC_SIZE];
bool success;
// float f = 0;
// float sum = 0;
// unsigned char * p;
unsigned long start;
unsigned long read_time;
unsigned long write_time = 0;

void setup() {
  coms_init();
}

void loop()
{
  if (Serial.available() > 0) {
    start = micros();
    success = read_from_pi(received);
    read_time = micros() - start;

    for (int i = 0; i < 20; i++) {
      send[i] = (char) received[i];
    }

    start = micros();
    write_to_pi(send);
    write_time = micros() - start;
    
    Serial.println(write_time);
    Serial.println(read_time);
    Serial.println(success);
  }
  // Serial.readBytes(received, 6);
  // delay(100);
}