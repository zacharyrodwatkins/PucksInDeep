#include <pi_coms.h>

uint8_t send[SEND_SIZE];  // 4 floats, 16 bytes
uint8_t received[REC_SIZE];
bool success;
float f = 0;
float sum = 0;
// unsigned char * p;
unsigned long start;
unsigned long read_time;
unsigned long write_time;

void setup() {
  coms_init();
}

void loop()
{
  for (int i=0; i<REC_SIZE; i++) {
  received[i] = 0;
  }
  sum = 0;
  if (Serial.available() == SEND_SIZE) {

    start = micros();
    success = read_from_pi(received);
    read_time = micros() - start;

    for (int i = 0; i < 16; i++) {
      send[i] = received[i];
    }
    for (int i = 0; i < 4; i++) {
      memcpy(&f, &(send[4*i]), 4);
      sum = sum + f;
    }
    memcpy(&send[16], &sum, 4);

    start = micros();
    write_to_pi(send);
    write_time = micros() - start;
    
    Serial.print(write_time);
    Serial.println(" ");
    Serial.print(read_time);
    Serial.println(" ");
    Serial.print(success);
    Serial.print("\n");

  }
}