//anchor #4 setup


// be sure to edit anchor_addr and select the previously calibrated anchor delay
// my naming convention is anchors 1, 2, 3, ... have the lowest order byte of the MAC address set to 81, 82, 83, ...

#include <SPI.h>
#include "DW1000Ranging.h"
#include "DW1000.h"

#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

String str_display = "80:17:5B:D5:A9:9A:E2:9C";;
String  anchorAddress = "";
char ANCHOR_ADD[24];
int Adelay = 0;
bool display_screen = false;

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


void setup()
{
  
  Serial.begin(115200);
  if(display_screen){
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
  }

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

void newRange()
{
  // 	// asymmetric two-way ranging (more computation intense, less error prone)
	// DW1000Time round1 = (DW1000Ranging.getDistantDevice()->timePollAckReceived-DW1000Ranging.getDistantDevice()->timePollSent).wrap();
	// DW1000Time reply1 = (DW1000Ranging.getDistantDevice()->timePollAckSent-DW1000Ranging.getDistantDevice()->timePollReceived).wrap();
	// DW1000Time round2 = (DW1000Ranging.getDistantDevice()->timeRangeReceived-DW1000Ranging.getDistantDevice()->timePollAckSent).wrap();
	// DW1000Time reply2 = (DW1000Ranging.getDistantDevice()->timeRangeSent-DW1000Ranging.getDistantDevice()->timePollAckReceived).wrap();

	// Serial.print("round1: "); Serial.println((long)round1.getTimestamp());
	
	// Serial.print("reply1: "); Serial.println((long)reply1.getTimestamp());
	
	// Serial.print("round2: "); Serial.println((long)round2.getTimestamp());
	
	// Serial.print("reply2: "); Serial.println((long)reply2.getTimestamp());

  // Serial.print("distance_meas: "); Serial.println(DW1000Ranging.getDistantDevice()->getRange());

  // Serial.print("distance_real: "); Serial.println(6.916);

    // /* Values that can be sent in binary */
  static DW1000Device *myDistantDevice = DW1000Ranging.getDistantDevice();
  uint16_t shortAddress = myDistantDevice->getShortAddress();
  float range = myDistantDevice->getRange();
  float RXPower = myDistantDevice->getRXPower();
  float FPPower = DW1000.getFirstPathPower();
  float quality = DW1000.getReceiveQuality();
  float timerpollsent = myDistantDevice->timePollSent.getAsMicroSeconds();
  float timerpollreceived = myDistantDevice->timePollAckReceived.getAsMicroSeconds();
  float timerpollacksent = myDistantDevice->timePollAckSent.getAsMicroSeconds();
  float timerpollackreceived = myDistantDevice->timePollAckReceived.getAsMicroSeconds();
  float timerrangesent = myDistantDevice->timeRangeSent.getAsMicroSeconds();
  float timerrangereceived = myDistantDevice->timeRangeReceived.getAsMicroSeconds();
  float timerino = millis();

  // Encodage en binaire des données
  size_t buffer_size = sizeof(shortAddress) + sizeof(range) + sizeof(RXPower) + sizeof(FPPower) + sizeof(quality) +
                      sizeof(timerpollsent) + sizeof(timerpollreceived) + sizeof(timerpollacksent) +
                      sizeof(timerpollackreceived) + sizeof(timerrangesent) + sizeof(timerrangereceived) +
                      sizeof(timerino);

  byte buffer[buffer_size];
  int offset = 0;
  memcpy(buffer + offset, &shortAddress, sizeof(shortAddress));
  offset += sizeof(shortAddress);
  memcpy(buffer + offset, &range, sizeof(range));
  offset += sizeof(range);
  memcpy(buffer + offset, &RXPower, sizeof(RXPower));
  offset += sizeof(RXPower);
  memcpy(buffer + offset, &FPPower, sizeof(FPPower));
  offset += sizeof(FPPower);
  memcpy(buffer + offset, &quality, sizeof(quality));
  offset += sizeof(quality);
  memcpy(buffer + offset, &timerpollsent, sizeof(timerpollsent));
  offset += sizeof(timerpollsent);
  memcpy(buffer + offset, &timerpollreceived, sizeof(timerpollreceived));
  offset += sizeof(timerpollreceived);
  memcpy(buffer + offset, &timerpollacksent, sizeof(timerpollacksent));
  offset += sizeof(timerpollacksent);
  memcpy(buffer + offset, &timerpollackreceived, sizeof(timerpollackreceived));
  offset += sizeof(timerpollackreceived);
  memcpy(buffer + offset, &timerrangesent, sizeof(timerrangesent));
  offset += sizeof(timerrangesent);
  memcpy(buffer + offset, &timerrangereceived, sizeof(timerrangereceived));
  offset += sizeof(timerrangereceived);
  memcpy(buffer + offset, &timerino, sizeof(timerino));
  offset += sizeof(timerino);

  // Envoi des données encodées sur le port série
  Serial.write(buffer, sizeof(buffer));

  
}

void newDevice(DW1000Device *device)
{
  // Serial.print("Device added: ");
  // Serial.println(device->getShortAddress(), HEX);
}

void inactiveDevice(DW1000Device *device)
{
  // Serial.print("Delete inactive device: ");
  // Serial.println(device->getShortAddress(), HEX);
}
