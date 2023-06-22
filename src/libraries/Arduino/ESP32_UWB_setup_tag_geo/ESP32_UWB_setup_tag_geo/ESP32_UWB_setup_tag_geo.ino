// currently tag is module #5
// The purpose of this code is to set the tag address and antenna delay to default.
// this tag will be used for calibrating the anchors.

#include <SPI.h>
#include "DW1000Ranging.h"
#include "DW1000.h"

#include <sstream>
#include <iomanip>

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

  //start the module as a tag, do not assign random short address
  DW1000Ranging.startAsTag(tag_addr, DW1000.MODE_LONGDATA_RANGE_LOWPOWER, false); 
}

// int incomingByte = 0; // for incoming serial data
void loop() {
  DW1000Ranging.loop();
}

//Default values
double latitude = 0;
double longitude = 0;
double depth = 0; // depth in meters
char lat_hem = (latitude > 0) ? 'N' : 'S';
char lon_hem = (longitude > 0) ? 'E' : 'W';
void get_geoloc(int beacon_id, double &longitude, double &latitude, double &depth, char &lat_hem, char &lon_hem){
  //Convertir beacon_id en hexadécimal
  std::stringstream converter;
  converter << std::hex << std::setw(4) << std::setfill('0') << beacon_id;
  std::string beacon_id_hex = converter.str();

  float alt_received = -0.0; //Given by the INS in real time (?)
  // float alt_gnss = -0.987;
  float alt_gnss = 0.177;
  float alt_uwb = 1.738;
  float red_b = 0.85; 
  // float alt_tag = -1.606;
  float offset = alt_uwb - alt_gnss; // - (alt_tag - alt_gnss); //La difference d'altitude entre l'antenne GNSS et l'antenne UWB

  if (beacon_id_hex == "1780") {
    // latitude = 48.89999011267607;
    // longitude = 2.0646126197183103;
    // depth = -92.16549295774645 + offset; // depth in- meters
    latitude = 48.899915;
    longitude = 2.064816;
    depth = - (93.01 + (offset - red_b));
    lat_hem = (latitude > 0) ? 'N' : 'S';
    lon_hem = (longitude > 0) ? 'E' : 'W';
  }

  if (beacon_id_hex == "1781") {
    // latitude = 48.90015534513275;
    // longitude = 2.0647127433628314;
    // depth = -93.44716814159293 + offset; // depth in- meters
    latitude = 48.899839;
    longitude = 2.065395;
    depth = - (91.885 + offset);
    lat_hem = (latitude > 0) ? 'N' : 'S';
    lon_hem = (longitude > 0) ? 'E' : 'W';
  }

  if (beacon_id_hex == "1782") {
    // latitude = 48.90029947586208;
    // longitude = 2.064277434482759;
    // depth = -93.00668965517241 + offset; // depth in- meters
    latitude = 48.90035918;
    longitude = 2.06422022;
    depth = - (91.50227848 + offset);
    lat_hem = (latitude > 0) ? 'N' : 'S';
    lon_hem = (longitude > 0) ? 'E' : 'W';
  }

  if (beacon_id_hex == "1783") {
    // latitude = 48.900285428571436;
    // longitude = 2.0639608333333332;
    // depth = -92.95414285714287 + offset; // depth in- meters
    latitude = 48.900252;
    longitude = 2.06391274;
    depth = - (91.6443299 + offset);
    lat_hem = (latitude > 0) ? 'N' : 'S';
    lon_hem = (longitude > 0) ? 'E' : 'W';
  }
}

void newRange() {
  /* Values that can be sent in ASCII */
  int beacon_id = DW1000Ranging.getDistantDevice()->getShortAddress();
  get_geoloc(beacon_id, longitude, latitude, depth, lat_hem, lon_hem);
  float beacon_range = DW1000Ranging.getDistantDevice()->getRange();
  float beacon_range_std_dev = 0.1;
  float age = ((float)millis() - (float)DW1000Ranging.getDistantDevice()->getValidTime())/1000; //millis()/1000 - (float)DW1000Ranging.getDistantDevice()->timeRangeSent.getTimestamp()*10
  
  // LLmm.mmmm to degrees and minutes conversion
  int lat_degrees = (int)latitude;
  float lat_minutes = (latitude - lat_degrees) * 60.0;
  // LLLmm.mmmm to degrees and minutes conversion
  int lon_degrees = (int)longitude;
  float lon_minutes = (fabs(longitude) - fabs(lon_degrees)) * 60.0;



  // construct the ASCII sentence
  char sentence[100];
  int sentence_length = sprintf(sentence, "$BFLBL,%02d%07.4f,%c,%03d%07.6f,%c,%.3f,%d,%.3f,%.3f,%.3f",
                                lat_degrees, lat_minutes, lat_hem,
                                lon_degrees, lon_minutes, lon_hem,
                                depth, beacon_id, beacon_range, beacon_range_std_dev, age);
  // calculate the checksum
  int checksum = 0;
  for (int i = 1; i < sentence_length; i++) {
      checksum ^= sentence[i];
  }

  // append the checksum and end-of-sentence characters
  sentence_length += sprintf(sentence + sentence_length, "*%02X\r\n", checksum);

  // send the sentence over serial
  dwSerial.print(sentence);
  
  // Serial.print(sentence);
  Serial.print("Get data from : ");
  Serial.print("Anchor : ");
  Serial.println(beacon_id);

                    // // // // // Faux capteur pour stocker les données de dbm -> LBL // // // // //

  int beacon_id2 = DW1000Ranging.getDistantDevice()->getShortAddress() - 6000;
  // get_geoloc(beacon_id, longitude, latitude, depth, lat_hem, lon_hem);
  float RXPower = -DW1000Ranging.getDistantDevice()->getRXPower(); //latitude
  float FPPower = -DW1000.getFirstPathPower(); //longitude
  float Quality = DW1000.getReceiveQuality(); //depth
  float RXFP =  DW1000Ranging.getDistantDevice()->getRXPower() - DW1000.getFirstPathPower(); //range
  float Quality2 = DW1000.getReceiveQuality2(); //beacon_range_std_dev
  
    // construct the ASCII sentence
  char sentence2[100];
  int sentence_length2 = sprintf(sentence2, "$BFLBL,%.3f,%c,%.3f,%c,%.3f,%d,%.3f,%.3f,%.3f",
                                FPPower, lat_hem,
                                RXPower, lon_hem,
                                Quality, beacon_id2, RXFP, Quality2, age);
  // calculate the checksum
  int checksum2 = 0;
  for (int i = 1; i < sentence_length2; i++) {
      checksum2 ^= sentence2[i];
  }

  // append the checksum and end-of-sentence characters
  sentence_length2 += sprintf(sentence2 + sentence_length2, "*%02X\r\n", checksum2);

  // send the sentence over serial
  dwSerial.print(sentence2);
  // Serial.print(sentence2);

}

void newDevice(DW1000Device *device) {
}

void inactiveDevice(DW1000Device *device) {
}




// TRASH
 // // Encodage en binaire des données
//   static DW1000Device *DistantDevice = DW1000Ranging.getDistantDevice();
// uint16_t shortAddress = DistantDevice->getShortAddress();
// int range = (int)(DistantDevice->getRange()*100);
// int RXPower = (int)(DistantDevice->getRXPower()*100);
// int FPPower = (int)(DW1000.getFirstPathPower()*100);
// int quality = (int)(DW1000.getReceiveQuality()*100);
// float timerpoll = DistantDevice->timePollSent.getAsMicroSeconds();
// float timersent = DistantDevice->timeRangeSent.getAsMicroSeconds();
// float timerino = millis();
// size_t buffer_size = sizeof(shortAddress) + sizeof(range) + sizeof(RXPower) + sizeof(FPPower) + sizeof(quality) + sizeof(timerpoll) + sizeof(timersent) + sizeof(timerino);
// byte buffer[buffer_size];
// int offset = 0;
// memcpy(buffer + offset, &shortAddress, sizeof(shortAddress));
// offset += sizeof(shortAddress);
// memcpy(buffer + offset, &range, sizeof(range));
// offset += sizeof(range);
// memcpy(buffer + offset, &RXPower, sizeof(RXPower));
// offset += sizeof(RXPower);
// memcpy(buffer + offset, &FPPower, sizeof(FPPower));
// offset += sizeof(FPPower);
// memcpy(buffer + offset, &quality, sizeof(quality));
// offset += sizeof(quality);
// memcpy(buffer + offset, &timerpoll, sizeof(timerpoll));
// offset += sizeof(timerpoll);
// memcpy(buffer + offset, &timersent, sizeof(timersent));
// offset += sizeof(timersent);
// memcpy(buffer + offset, &timerino, sizeof(timerino));
// offset += sizeof(timerino);

// // Envoi des données encodées sur le port série
// Serial.write(buffer, sizeof(buffer));
