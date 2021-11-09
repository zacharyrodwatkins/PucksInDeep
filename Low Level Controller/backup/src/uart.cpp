#include <Arduino.h>

HardwareSerial Serial3(PB11, PB10);
int readByte;
int writeByte = 16;

void setup() {
    Serial3.begin(9600);
    Serial.begin(9600);
}

void loop() {
    readByte = Serial3.read();
    if (readByte != -1) {
        Serial.println(Serial3.read());
        Serial3.write(writeByte);
    } else {
        Serial3.write(0);
    }
}