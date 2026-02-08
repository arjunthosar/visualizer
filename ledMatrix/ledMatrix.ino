
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
  matrix->Color(255, 0, 0),
  matrix->Color(255, 0, 0),
  matrix->Color(255, 25, 0),
  matrix->Color(255, 49, 0),
  matrix->Color(255, 74, 0),
  matrix->Color(255, 99, 0),
  matrix->Color(255, 123, 0),
  matrix->Color(255, 148, 0),
  matrix->Color(255, 173, 0),
  matrix->Color(255, 197, 0),
  matrix->Color(255, 222, 0),
  matrix->Color(255, 247, 0),
  matrix->Color(239, 255, 0),
  matrix->Color(214, 255, 0),
  matrix->Color(189, 255, 0),
  matrix->Color(165, 255, 0),
  matrix->Color(140, 255, 0),
  matrix->Color(115, 255, 0),
  matrix->Color(90, 255, 0),
  matrix->Color(66, 255, 0),
  matrix->Color(41, 255, 0),
  matrix->Color(16, 255, 0),
  matrix->Color(0, 255, 8),
  matrix->Color(0, 255, 33),
  matrix->Color(0, 255, 58),
  matrix->Color(0, 255, 82),
  matrix->Color(0, 255, 107),
  matrix->Color(0, 255, 132),
  matrix->Color(0, 255, 156),
  matrix->Color(0, 255, 181),
  matrix->Color(0, 255, 206),
  matrix->Color(0, 255, 230),
  matrix->Color(0, 255, 255)
};

void setup() {
  Serial.begin(9600);
  Serial.setTimeout(5);
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
        matrix->drawFastVLine(i+1, 0, num, colors[i]);
      }
      matrix->show();
  
  }
}
