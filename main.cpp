// Companion file to the Segger Embedded Studio HelloWorld Example
// Simply blinks the LED on the target development board

#include "mbed.h"
// Blinking rate in milliseconds

DigitalOut led(LED1) = true;

int main() {
  while (true) {
    ThisThread::sleep_for(500ms);
    led = !led;
  }
}
