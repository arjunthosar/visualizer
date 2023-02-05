
#include <Adafruit_GFX.h>
#include <Adafruit_NeoMatrix.h>
#include <Adafruit_NeoPixel.h>

#define PIN 6
int num;
int prevVals[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};

Adafruit_NeoMatrix *matrix = new Adafruit_NeoMatrix(32, 8, PIN,
  NEO_MATRIX_BOTTOM     + NEO_MATRIX_LEFT +
  NEO_MATRIX_COLUMNS + NEO_MATRIX_ZIGZAG,
  NEO_GRB            + NEO_KHZ800);

const uint16_t colors[] = {
  0x0F00 };

void setup() {
  Serial.begin(9600);
  Serial.setTimeout(10);
  matrix->begin();
  matrix->setBrightness(5);
}

void loop() {
  if (Serial.available() > 0) {
    matrix->clear();
      String strengths=Serial.readString();
      for (int i=0; i<32; i+=1) {
        num=String(strengths[i+2]).toInt();
        if (num==0) {
          continue;
        }
        matrix->drawFastVLine(i, 0, num, colors[0]);
      }
      matrix->show();
  
  }
}
