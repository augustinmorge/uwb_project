//anchor #4 setup


// be sure to edit anchor_addr and select the previously calibrated anchor delay
// my naming convention is anchors 1, 2, 3, ... have the lowest order byte of the MAC address set to 81, 82, 83, ...

#include <SPI.h>
#include "DW1000Ranging.h"
#include "DW1000.h"

#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

int selected_anchor = 83;
String str_display = "";
String  anchorAddress = "";
char ANCHOR_ADD[24];
int Adelay = 0;

// previously determined calibration results for antenna delay
// #1 16520
// #2 16539
// #3 16545
// #4 16505

// calibration distance
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

void starting_parameters(){
  switch(selected_anchor){
    case 80:
      anchorAddress = "80:17:5B:D5:A9:9A:E2:9C";
      anchorAddress.toCharArray(ANCHOR_ADD, 24);
      // Adelay = 16520;
      Adelay = 16535;
      str_display =  "UWB Anchor 80 ";
      break;
    case 81:
      anchorAddress = "81:17:5B:D5:A9:9A:E2:9C";
      anchorAddress.toCharArray(ANCHOR_ADD, 24);
      // Adelay = 16539;
      Adelay = 16550;
      str_display =  "UWB Anchor 81 ";
      break;
    case 82:
      anchorAddress = "82:17:5B:D5:A9:9A:E2:9C";
      anchorAddress.toCharArray(ANCHOR_ADD, 24);
      Adelay = 16445;
      str_display =  "UWB Anchor 82 ";
      break;
    case 83:
      anchorAddress = "83:17:5B:D5:A9:9A:E2:9C";
      anchorAddress.toCharArray(ANCHOR_ADD, 24);
      // Adelay = 16505;
      Adelay = 16540;
      str_display =  "UWB Anchor 83 ";
      break;
    default:
      anchorAddress = "80:17:5B:D5:A9:9A:E2:9C";
      anchorAddress.toCharArray(ANCHOR_ADD, 24);
      Adelay = 16530;
      str_display =  "UWB Anchor 80 ";
      break;
  }
}

void setup()
{
  starting_parameters();
  
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

    display.println(str_display);
    display.display();

  delay(1000); //wait for serial monitor to connect
  Serial.println("Anchor config and start");
  Serial.print("Antenna delay ");
  Serial.println(Adelay);

  //init the configuration
  SPI.begin(SPI_SCK, SPI_MISO, SPI_MOSI);
  DW1000Ranging.initCommunication(PIN_RST, PIN_SS, PIN_IRQ); //Reset, CS, IRQ pin

  // set antenna delay for anchors only. Tag is default (16384)
  DW1000.setAntennaDelay(Adelay);

  DW1000Ranging.attachNewRange(newRange);
  DW1000Ranging.attachNewDevice(newDevice);
  DW1000Ranging.attachInactiveDevice(inactiveDevice);

  //start the module as an anchor, do not assign random short address
  DW1000Ranging.startAsAnchor(ANCHOR_ADD, DW1000.MODE_LONGDATA_RANGE_LOWPOWER, false);
  // DW1000Ranging.startAsAnchor(ANCHOR_ADD, DW1000.MODE_SHORTDATA_FAST_LOWPOWER,false);
  // DW1000Ranging.startAsAnchor(ANCHOR_ADD, DW1000.MODE_LONGDATA_FAST_LOWPOWER,false);
  // DW1000Ranging.startAsAnchor(ANCHOR_ADD, DW1000.MODE_SHORTDATA_FAST_ACCURACY,false);
  // DW1000Ranging.startAsAnchor(ANCHOR_ADD, DW1000.MODE_LONGDATA_FAST_ACCURACY,false);
  // DW1000Ranging.startAsAnchor(ANCHOR_ADD, DW1000.MODE_LONGDATA_RANGE_ACCURACY, false);
}

// const byte DW1000Class::MODE_LONGDATA_RANGE_LOWPOWER[] = {TRX_RATE_110KBPS, TX_PULSE_FREQ_16MHZ, TX_PREAMBLE_LEN_2048};
// const byte DW1000Class::MODE_SHORTDATA_FAST_LOWPOWER[] = {TRX_RATE_6800KBPS, TX_PULSE_FREQ_16MHZ, TX_PREAMBLE_LEN_128};
// const byte DW1000Class::MODE_LONGDATA_FAST_LOWPOWER[]  = {TRX_RATE_6800KBPS, TX_PULSE_FREQ_16MHZ, TX_PREAMBLE_LEN_1024};
// const byte DW1000Class::MODE_SHORTDATA_FAST_ACCURACY[] = {TRX_RATE_6800KBPS, TX_PULSE_FREQ_64MHZ, TX_PREAMBLE_LEN_128};
// const byte DW1000Class::MODE_LONGDATA_FAST_ACCURACY[]  = {TRX_RATE_6800KBPS, TX_PULSE_FREQ_64MHZ, TX_PREAMBLE_LEN_1024};
// const byte DW1000Class::MODE_LONGDATA_RANGE_ACCURACY[] = {TRX_RATE_110KBPS, TX_PULSE_FREQ_64MHZ, TX_PREAMBLE_LEN_2048};
void loop()
{
  DW1000Ranging.loop();
}

// float t0 = millis();
void newRange()
{
  //    Serial.print("from: ");
  // Serial.print(DW1000Ranging.getDistantDevice()->getShortAddress(), HEX);
  // Serial.print(", ");

#define NUMBER_OF_DISTANCES 1
  float dist = 0.0;
  for (int i = 0; i < NUMBER_OF_DISTANCES; i++) {
    dist += DW1000Ranging.getDistantDevice()->getRange();
  }
  dist = dist/NUMBER_OF_DISTANCES;
  Serial.print(dist);
  Serial.println(", ");
  // Serial.println(DW1000Ranging.getDistantDevice()->getRXPower());
  // Serial.print(", ");
  // Serial.print(DW1000Ranging.getDistantDevice()->getFPPower());
  // Serial.print(", diff:");
  // Serial.println(DW1000Ranging.getDistantDevice()->getRXPower() - DW1000Ranging.getDistantDevice()->getFPPower());
  // Serial.print(", ");
  // Serial.println(DW1000.getReceiveQuality());
  // Serial.println("");
  // Serial.println(millis() - t0);
  // t0 = millis();
}

void newDevice(DW1000Device *device)
{
  Serial.print("Device added: ");
  Serial.println(device->getShortAddress(), HEX);
}

void inactiveDevice(DW1000Device *device)
{
  Serial.print("Delete inactive device: ");
  Serial.println(device->getShortAddress(), HEX);
}
