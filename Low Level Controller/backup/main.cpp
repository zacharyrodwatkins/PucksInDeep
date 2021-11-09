#include <SPI.h>
#include <Arduino.h>
#include "pins_arduino.h"
// SPI slave example
// STM32 acts as a SPI slave an reads 8 bit data frames over SPI
// The data sent to the master is a simple count (0, 1, 2, 3) that is incremented
// each time a data frame is received.
// Serial output is here for debug
// #include

void setupSPI(void)
{
  // MOSI, MISO, SCK PINs are set by the library
  pinMode(A4, INPUT); // SS
  // The clock value is not used
  // SPI1 is selected by default
  SPI.beginTransactionSlave(SPISettings(18000000, MSBFIRST, SPI_MODE0));
}
void setup()
{
  Serial.begin(9600);
  delay(100);
  setupSPI();
}
uint8_t count(0);
void loop()
{
  // Blocking call to read SPI message
  uint8_t msg(SPI.transfer(++count));
  Serial.print("Received = 0b");
  Serial.print(msg, BIN);
  Serial.print(", 0x");
  Serial.print(msg, HEX);
  Serial.print(", ");
  Serial.println(msg);
}

// char buf [100];
// volatile byte pos;
// volatile boolean process_it;

// void setup (void)
// {
//   Serial.begin (9600);   // debugging

//   // have to send on master in, *slave out*
//   pinMode(MISO, OUTPUT);
  
//   // turn on SPI in slave mode
//   SPCR |= _BV(SPE);
  
//   // turn on interrupts
//   SPCR |= _BV(SPIE);
  
//   pos = 0;
//   process_it = false;
// }  // end of setup


// // SPI interrupt routine
// ISR (SPI_STC_vect) {
// byte c = SPDR;
  
//   // add to buffer if room
//   if (pos < sizeof buf) {
//     buf [pos++] = c;
  
//     // example: newline means time to process buffer
//     if (c == '\n') {
//       process_it = true;
      
//     }  // end of room available
//   }
// }


// // main loop - wait for flag set in interrupt routine
// void loop (void)
// {
//   if (process_it)
//     {
//     buf [pos] = 0;  
//     Serial.println (buf);
//     pos = 0;
//     process_it = false;
//     }  // end of flag set
    
// }  // end of loop

void SPIConfig (void)
{
  RCC->APB2ENR |= (1<<12);  // Enable SPI1 CLock
	
  SPI1->CR1 |= (1<<0)|(1<<1);   // CPOL=1, CPHA=1
	
  SPI1->CR1 |= (1<<2);  // Master Mode
	
  SPI1->CR1 |= (3<<3);  // BR[2:0] = 011: fPCLK/16, PCLK2 = 80MHz, SPI clk = 5MHz
	
  SPI1->CR1 &= ~(1<<7);  // LSBFIRST = 0, MSB first
	
  SPI1->CR1 |= (1<<8) | (1<<9);  // SSM=1, SSi=1 -> Software Slave Management
	
  SPI1->CR1 &= ~(1<<10);  // RXONLY = 0, full-duplex
	
  SPI1->CR1 &= ~(1<<11);  // DFF=0, 8 bit data
	
  SPI1->CR2 = 0;
}