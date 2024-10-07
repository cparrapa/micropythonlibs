#include <Adafruit_NeoPixel.h>
 
const int RgbPin = D1;
const int SingPin = D2;
float distance;
unsigned long Time_Echo_us = 0;
 

Adafruit_NeoPixel usrgb = Adafruit_NeoPixel(6,D1, NEO_GRB + NEO_KHZ800);
long ultrasound_distance() {
   long Time_Echo_us, distance;
   pinMode(D2, OUTPUT);
   digitalWrite(D2, LOW);
   delayMicroseconds(2);
   digitalWrite(D2, HIGH);
   delayMicroseconds(20);
   digitalWrite(D2, LOW);
    pinMode(D2, INPUT);
   Time_Echo_us = pulseIn(D2, HIGH);
if ((Time_Echo_us < 60000) && (Time_Echo_us > 1)) {
distance = Time_Echo_us / 58.00;
}
delay(200);
   return distance;
}
 

void setup() {
  Serial.begin(9600);
 
  pinMode(D2, OUTPUT);
 
  usrgb.begin();
usrgb.clear();
usrgb.fill( usrgb.Color(0, 255, 255));
usrgb.show();
 

}
 
void loop() {
    Serial.print("Ultrasonic sensor reading:");
    Serial.print(ultrasound_distance());
    Serial.print("cm");
    Serial.println("");
 
}