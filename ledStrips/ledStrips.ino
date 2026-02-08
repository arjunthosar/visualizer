#include <Adafruit_NeoPixel.h>


#define NUMPIXELS 8
Adafruit_NeoPixel one(NUMPIXELS, 6, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel two(NUMPIXELS, 5, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel three(NUMPIXELS, 4, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel four(NUMPIXELS, 3, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel five(NUMPIXELS, 2, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel pixels[] = {one, two, three, four, five};
uint32_t colors[] = {one.Color(10, 0, 255), two.Color(0, 25, 255), three.Color(8, 255, 0), four.Color(25, 255, 0)};  // Maybe switch colors other way around (rainbow)
int prevVals[] = {0, 0, 0, 0};
#define DELAYVAL 0
int num;

void setup() {
  // Initialize serial communication
  Serial.begin(9600);
  Serial.setTimeout(1/0.3);
//  one.begin();
//  two.begin();
  for (int i=0; i<5; i++) {
    pixels[i].begin();
  }
  pixels[0].setBrightness(150);
  pixels[1].setBrightness(150);
  pixels[2].setBrightness(40);
  pixels[3].setBrightness(40);
}

void loop() {
  if (Serial.available() > 0) {
    String strengths=Serial.readString();
    for (int i=1; i<11; i+=2) {
      pixels[(i-1)/2].clear();
      num=String(strengths[i+1]).toInt();
      if (num != 0) {
        pixels[(i-1)/2].fill(colors[(i-1)/2], 0, num);
        prevVals[(i-1)/2]=num;        
      } else {
        prevVals[(i-1)/2]=0;
      }
      pixels[(i-1)/2  ].show();
    }
  }
}
