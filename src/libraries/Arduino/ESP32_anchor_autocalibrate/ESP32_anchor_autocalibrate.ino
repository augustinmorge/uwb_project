// This program calibrates an ESP32_UWB module intended for use as a fixed anchor point
// uses binary search to find anchor antenna delay to calibrate against a known distance
//
// modified version of Thomas Trojer's DW1000 library is required!

// Remote tag (at origin) must be set up with default antenna delay (library default = 16384)

// user input required, possibly unique to each tag:
// 1) accurately measured distance from anchor to tag
// 2) address of anchor
//
// output: antenna delay parameter for use in final anchor setup.
// S. James Remington 2/20/2022

#include <SPI.h>
#include "DW1000Ranging.h"
#include "DW1000.h"

#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
// ESP32_UWB pin definitions

#define SPI_SCK 18
#define SPI_MISO 19
#define SPI_MOSI 23

// connection pins
#define PIN_RST 27 // reset pin
#define PIN_IRQ 34 // irq pin
#define PIN_SS 21   // spi select pin


#define I2C_SDA 4
#define I2C_SCL 5

Adafruit_SSD1306 display(128, 64, &Wire, -1);

#define ANCHOR_ADD "81:17:5B:D5:A9:9A:E2:9C"
float this_anchor_target_distance = 2; //measured distance to anchor in m

float this_anchor_Adelay = 15000; //starting value
float Adelay_delta = 100; //initial binary search step size


void setup()
{
  Serial.begin(115200);

  //Init the screen 
    Wire.begin(I2C_SDA, I2C_SCL);
    delay(1000);
    // SSD1306_SWITCHCAPVCC = generate display voltage from 3.3V internally
    if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C))
    { // Address 0x3C for 128x32
        Serial.println(F("SSD1306 allocation failed"));
        for (;;)
            ; // Don't proceed, loop forever
    }
    display.clearDisplay();
    display.setTextSize(2);      // Normal 1:1 pixel scale
    display.setTextColor(SSD1306_WHITE); // Draw white text
    display.setCursor(0, 0);     // Start at top-left corner

    display.println("UWB Anchor 80 ");
    display.display();

  while (!Serial);
  //init the configuration
  SPI.begin(SPI_SCK, SPI_MISO, SPI_MOSI);
  DW1000Ranging.initCommunication(PIN_RST, PIN_SS, PIN_IRQ); //Reset, CS, IRQ pin


  Serial.print("Starting Adelay "); Serial.println(this_anchor_Adelay);
  Serial.print("Measured distance "); Serial.println(this_anchor_target_distance);
  
  DW1000.setAntennaDelay(this_anchor_Adelay);

  DW1000Ranging.attachNewRange(newRange);
  DW1000Ranging.attachNewDevice(newDevice);
  DW1000Ranging.attachInactiveDevice(inactiveDevice);
  //Enable the filter to smooth the distance
  //DW1000Ranging.useRangeFilter(true);

  //start the module as anchor, don't assign random short address
  DW1000Ranging.startAsAnchor(ANCHOR_ADD, DW1000.MODE_LONGDATA_RANGE_LOWPOWER, false);

}

void loop()
{
  DW1000Ranging.loop();
}

int tot = 0;
float anchor_delay_final = 0;
void newRange()
{
  static float last_delta = 0.0;
  // Serial.print(DW1000Ranging.getDistantDevice()->getShortAddress(), DEC);

  float dist = 0;
  for (int i = 0; i < 100; i++) {
    // get and average 100 measurements
    dist += DW1000Ranging.getDistantDevice()->getRange();
  }
  dist /= 100.0;

  // Serial.print(",");
  Serial.println(dist); 
  if (Adelay_delta < 3) {
    if(tot==100){while (1);}
    Serial.print("final Adelay n°");
    Serial.print(tot);
    Serial.print(": ");
    tot ++;
    anchor_delay_final = anchor_delay_final + this_anchor_Adelay;
    Serial.println(anchor_delay_final/tot);
//    Serial.print("Check: stored Adelay = ");
//    Serial.println(DW1000.getAntennaDelay());
  Adelay_delta = 100;
    // while(1);  //done calibrating
  }

  float this_delta = dist - this_anchor_target_distance;  //error in measured distance

  if ( this_delta * last_delta < 0.0) Adelay_delta = Adelay_delta / 2; //sign changed, reduce step size
    last_delta = this_delta;
  
  if (this_delta > 0.0 ) this_anchor_Adelay += Adelay_delta; //new trial Adelay
  else this_anchor_Adelay -= Adelay_delta;
  
  // Serial.print(", Adelay = ");
  // Serial.println (this_anchor_Adelay);
  // SPI.begin(SPI_SCK, SPI_MISO, SPI_MOSI);
  // DW1000Ranging.initCommunication(PIN_RST, PIN_SS, PIN_IRQ); //Reset, CS, IRQ pin
  DW1000.setAntennaDelay(this_anchor_Adelay);

  // if ((this_anchor_Adelay < 16400) or (this_anchor_Adelay > 16800)){this_anchor_Adelay = 16400; delay(500);}
}

void newDevice(DW1000Device *device)
{
  Serial.print("Device added: ");
  Serial.println(device->getShortAddress(), HEX);
}

void inactiveDevice(DW1000Device *device)
{
  Serial.print("delete inactive device: ");
  Serial.println(device->getShortAddress(), HEX);
}
