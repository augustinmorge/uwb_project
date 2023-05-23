// currently tag is module #5
// The purpose of this code is to set the tag address and antenna delay to default.
// this tag will be used for calibrating the anchors.

// #include <SPI.h>
#include "DW1000Ranging.h"
#include "DW1000.h"

// #define SPI_SCK 18
// #define SPI_MISO 19
// #define SPI_MOSI 23

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
  // SPI.begin(SPI_SCK, SPI_MISO, SPI_MOSI);
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

// int incomingByte = 0; // for incoming serial data
void loop() {
  DW1000Ranging.loop();

  /* Time */
  // Serial.print("timePollSent: ");Serial.println((double)DW1000Ranging.getDistantDevice()->timePollSent.getAsMicroSeconds());

  // Serial.print("timeRangeSent: ");Serial.println((double)DW1000Ranging.getDistantDevice()->timeRangeSent.getAsMicroSeconds());

  // Serial.print("timeINO: " ); Serial.println(millis());
}

float _delay = 0;
int ct_delay = 1;
float t_delay = millis();
void newRange() {
  /* Values that can be displayed */
  // Serial.print("from: ");
  // Serial.print(DW1000Ranging.getDistantDevice()->getShortAddress(), HEX);
  // Serial.print("\t Range: ");
  // Serial.println(DW1000Ranging.getDistantDevice()->getRange());
  // Serial.print(" m");
  // Serial.print("\t RX power: ");
  // Serial.print(DW1000Ranging.getDistantDevice()->getRXPower());
  // Serial.print(" dBm");
  // Serial.print("\t FP power: ");
  // Serial.print(DW1000.getFirstPathPower());
  // Serial.print(" dBm");
  // Serial.print("\t Quality: ");
  // Serial.print(DW1000.getReceiveQuality());
  // Serial.print("\t Timer: ");
  // long unsigned int timer = millis();
  // DW1000Time val = DW1000Ranging.getDistantDevice()->timeRangeSent;
  // double timer = (double) val.getTimestamp() * 1e-11;
  // Serial.println(timer);

  static DW1000Device *DistantDevice = DW1000Ranging.getDistantDevice();

  /* Values that can be sent in binary */
  uint16_t shortAddress = DistantDevice->getShortAddress();
  int range = (int)(DistantDevice->getRange()*100);
  int RXPower = (int)(DistantDevice->getRXPower()*100);
  int FPPower = (int)(DW1000.getFirstPathPower()*100);
  int quality = (int)(DW1000.getReceiveQuality()*100);
  float timerpoll = DistantDevice->timePollSent.getAsMicroSeconds();
  float timersent = DistantDevice->timeRangeSent.getAsMicroSeconds();
  float timerino = millis();

  // Encodage en binaire des données
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

  /* Values that can be sent in ASCII */
  // double latitude = 48.5357;
  // double longitude = 2.0350;
  // double depth = 10.5; // depth in meters
  // char lat_hem = (latitude > 0) ? 'N' : 'S';
  // char lon_hem = (longitude > 0) ? 'E' : 'W';
  // float beacon_range = DW1000Ranging.getDistantDevice()->getRange();
  // // Serial.print("range: "); Serial.println(beacon_range);
  // float beacon_range_std_dev = 0.1;
  // float age = 0 ; //millis()/1000 - (float)DW1000Ranging.getDistantDevice()->timeRangeSent.getTimestamp()*10
  // int beacon_id = 80;

  // // LLmm.mmmm to degrees and minutes conversion
  // int lat_degrees = (int)latitude;
  // float lat_minutes = (latitude - lat_degrees) * 60.0;
  // // LLLmm.mmmm to degrees and minutes conversion
  // int lon_degrees = (int)longitude;
  // float lon_minutes = (fabs(longitude) - fabs(lon_degrees)) * 60.0;



  // // construct the ASCII sentence
  // char sentence[100];
  // int sentence_length = sprintf(sentence, "$BFLBL,%02d%07.4f,%c,%03d%07.6f,%c,%.3f,%d,%.3f,%.3f,%.3f",
  //                               lat_degrees, lat_minutes, lat_hem,
  //                               lon_degrees, lon_minutes, lon_hem,
  //                               depth, beacon_id, beacon_range, beacon_range_std_dev, age);
  // // calculate the checksum
  // Serial.println(sentence);
  // int checksum = 0;
  // for (int i = 1; i < sentence_length; i++) {
  //     checksum ^= sentence[i];
  // }

  // // append the checksum and end-of-sentence characters
  // sentence_length += sprintf(sentence + sentence_length, "*%02X\r\n", checksum);

  // // send the sentence over serial
  // dwSerial.print(sentence);

  // delay(1000);
}

void newDevice(DW1000Device *device) {
  // Serial.print("Device added: ");
  // Serial.println(device->getShortAddress(), HEX);
}

void inactiveDevice(DW1000Device *device) {
  // Serial.print("delete inactive device: ");
  // Serial.println(device->getShortAddress(), HEX);
}
