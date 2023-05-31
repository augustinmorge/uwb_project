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

  if (beacon_id_hex == "1780") {
    latitude = 48.5357;
    longitude = 2.0350;
    depth = 0.5; // depth in meters
    lat_hem = (latitude > 0) ? 'N' : 'S';
    lon_hem = (longitude > 0) ? 'E' : 'W';
  }

  if (beacon_id_hex == "1781") {
    latitude = 48.535927083;
    longitude = 2.035399667;
    depth = 0.5; // depth in meters
    lat_hem = (latitude > 0) ? 'N' : 'S';
    lon_hem = (longitude > 0) ? 'E' : 'W';
  }

  if (beacon_id_hex == "1782") {
    latitude = 48.5357;
    longitude = 2.0350;
    depth = 10.5; // depth in meters
    lat_hem = (latitude > 0) ? 'N' : 'S';
    lon_hem = (longitude > 0) ? 'E' : 'W';
  }

  if (beacon_id_hex == "1783") {
    latitude = 48.5425177;
    longitude = 2.034726171;
    depth = 0.5; // depth in meters
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
  float age = 0.045 ; //millis()/1000 - (float)DW1000Ranging.getDistantDevice()->timeRangeSent.getTimestamp()*10
  
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
  Serial.print(sentence);
}

void newDevice(DW1000Device *device) {
}

void inactiveDevice(DW1000Device *device) {
}
