#include <pi_coms.h>

void coms_init() {
  Serial.begin(1000000);
  Serial.setTimeout(1);
  delay(100);
}

bool read_from_pi(byte *buffer) {
  // start = micros();
  float f;
  float sum;
  Serial.readBytesUntil('\n', buffer, REC_SIZE);
  for (int i = 0; i < 4; i++) {
    memcpy(&f, &(buffer[4*i]), 4);
    sum = sum + f;
  }
  memcpy(&f, &(buffer[16]), 4);
  if (abs(sum-f) < 0.0001) {
    return true;
  }
  return false;
  // read_time = micros() - start;
}

void write_to_pi(char *buffer) {
  // start = micros();
  for (int i = 0; i<SEND_SIZE; i++) {
    Serial.write(buffer[i]);
  }
  Serial.write("\n");
  // write_time = micros() - start;
}
