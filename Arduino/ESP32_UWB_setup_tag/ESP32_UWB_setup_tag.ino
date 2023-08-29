// currently tag is module #5
// The purpose of this code is to set the tag address and antenna delay to default.
// this tag will be used for calibrating the anchors.

#include <SPI.h>
#include "DW1000Ranging.h"
#include "DW1000.h"

#define SPI_SCK 18
#define SPI_MISO 19
#define SPI_MOSI 23

// connection pins
const uint8_t PIN_RST = 27;  // reset pin
const uint8_t PIN_IRQ = 34;  // irq pin
const uint8_t PIN_SS = 21;   // spi select pin

// TAG antenna delay defaults to 16384
// leftmost two bytes below will become the "short address"
char tag_addr[] = "7D:00:22:EA:82:60:3B:9C";

// Configure serial COM RX/TX
#define DW1000_RX_PIN 25     // Replace with the appropriate RX pin number
#define DW1000_TX_PIN 26     // Replace with the appropriate TX pin number
HardwareSerial dwSerial(1);  // Use UART 1
const int baudRate = 115200;

void setup() {
  //Setup serial RX/TX
  dwSerial.begin(baudRate, SERIAL_8N1, DW1000_RX_PIN, DW1000_TX_PIN);

  //Setup console
  Serial.begin(115200);
  delay(1000);

  //init the configuration
  SPI.begin(SPI_SCK, SPI_MISO, SPI_MOSI);
  DW1000Ranging.initCommunication(PIN_RST, PIN_SS, PIN_IRQ);  //Reset, CS, IRQ pin

  DW1000Ranging.attachNewRange(newRange);
  DW1000Ranging.attachNewDevice(newDevice);
  DW1000Ranging.attachInactiveDevice(inactiveDevice);

  // start as tag, do not assign random short address

  //start the module as a tag, do not assign random short address
  DW1000Ranging.startAsTag(tag_addr, DW1000.MODE_LONGDATA_RANGE_LOWPOWER, false);
  // DW1000Ranging.startAsTag(tag_addr, DW1000.MODE_SHORTDATA_FAST_LOWPOWER,false);
  // DW1000Ranging.startAsTag(tag_addr, DW1000.MODE_LONGDATA_FAST_LOWPOWER,false);
  // DW1000Ranging.startAsTag(tag_addr, DW1000.MODE_SHORTDATA_FAST_ACCURACY,false);
  // DW1000Ranging.startAsTag(tag_addr, DW1000.MODE_LONGDATA_FAST_ACCURACY,false);
  // DW1000Ranging.startAsTag(tag_addr, DW1000.MODE_LONGDATA_RANGE_ACCURACY, false);
}

float timerino = millis();
void loop() {
  DW1000Ranging.loop();
  timerino = millis();
}

void newRange() {
  /* Values that can be displayed */
  // Serial.print("from: ");
  // Serial.println(DW1000Ranging.getDistantDevice()->getShortAddress(), HEX);
  // Serial.print("\t Range: ");
  // Serial.print(DW1000Ranging.getDistantDevice()->getRange());
  // Serial.print(" m");
  // Serial.print("\t RX power: ");
  // Serial.print(DW1000Ranging.getDistantDevice()->getRXPower());
  // Serial.print(" dBm");
  // Serial.print("\t FP power: ");
  // Serial.print(DW1000.getFirstPathPower());
  // float RXFP = DW1000.getReceivePower() - DW1000.getFirstPathPower();
  // if(DW1000Ranging.getDistantDevice()->getShortAddress() == 6017){
  //   Serial.println("FP power - RX power [TAG not filtered]: ");
  //   Serial.println(RXFP);
  //   Serial.println("FP power - RX power [TAG filtered]: ");
  //   float corrFac = 2.3334;
  //   float RX = DW1000Ranging.getDistantDevice()->getRXPower();
  //   float FP = DW1000.getFirstPathPower();
  //   bool with_filter = false;
  //   if (!with_filter){
  //     Serial.println("RX");
  //     if(RX <= - 88){
  //       RX = RX;
  //     }
  //     else{
  //       RX += (RX + 88)*corrFac;
  //     }
  //   }
  //   if (!with_filter){
  //     Serial.println("FP");
  //     if(FP <= - 88){
  //       FP = FP;
  //     }
  //     else{
  //       FP += (FP + 88)*corrFac;
  //     }
  //   }
  //   Serial.println(RX - FP);
  //   Serial.println("FP power - RX power [ANCHOR]: ");
  //   Serial.println(DW1000Ranging.getDistantDevice()->getRXPower() - DW1000.getFirstPathPower());
  //   Serial.println();

  // }

  // Serial.print(" dBm");
  // Serial.print("\t Quality: ");
  // Serial.print(DW1000.getReceiveQuality2());
  // Serial.print("\t delay: ");
  // Serial.println(millis() - DW1000Ranging.getDistantDevice()->getValidTime());

  /* Values that can be sent in binary */
  uint16_t shortAddress = DW1000Ranging.getDistantDevice()->getShortAddress();
  // int range = (int)(DW1000Ranging.getDistantDevice()->getRange()*100);
  // int RXPower = (int)(DW1000Ranging.getDistantDevice()->getRXPower()*100);
  // int FPPower = (int)(DW1000.getFirstPathPower()*100);
  // int quality = (int)(DW1000.getReceiveQuality()*100);
  float range = DW1000Ranging.getDistantDevice()->getRange();
  float RXPower = DW1000Ranging.getDistantDevice()->getRXPower();
  float FPPower = DW1000.getFirstPathPower();
  float quality = DW1000.getReceiveQuality();
  float timerpoll = DW1000Ranging.getDistantDevice()->timePollSent.getAsMicroSeconds();
  float timersent = DW1000Ranging.getDistantDevice()->timeRangeSent.getAsMicroSeconds();
  

  size_t buffer_size = sizeof(shortAddress) + sizeof(range) + sizeof(RXPower) + sizeof(FPPower) + sizeof(quality) + sizeof(timerpoll) + sizeof(timersent) + sizeof(timerino);
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
  memcpy(buffer + offset, &timerpoll, sizeof(timerpoll));
  offset += sizeof(timerpoll);
  memcpy(buffer + offset, &timersent, sizeof(timersent));
  offset += sizeof(timersent);
  memcpy(buffer + offset, &timerino, sizeof(timerino));
  offset += sizeof(timerino);

  // Envoi des données encodées sur le port série
  Serial.write(buffer, sizeof(buffer));

}

void newDevice(DW1000Device *device) {
  // Serial.print("Device added: ");
  // Serial.println(device->getShortAddress(), HEX);
}

void inactiveDevice(DW1000Device *device) {
  // Serial.print("delete inactive device: ");
  // Serial.println(device->getShortAddress(), HEX);
}
