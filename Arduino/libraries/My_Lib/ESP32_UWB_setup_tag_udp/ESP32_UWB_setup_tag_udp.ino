/*

For ESP32 UWB or ESP32 UWB Pro

*/

#include <SPI.h>
#include <DW1000Ranging.h>

#include <WiFi.h>
#include "link.h"

#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define TAG_ADDR "7D:00:22:EA:82:60:3B:9B"

#define SPI_SCK 18
#define SPI_MISO 19
#define SPI_MOSI 23

#define UWB_RST 27 // reset pin
#define UWB_IRQ 34 // irq pin
#define UWB_SS 21   // spi select pin

#define I2C_SDA 4
#define I2C_SCL 5

const char *ssid = "iXGuest";
const char *password = "URWelcome";
const char *host = "10.123.0.132"; //10.123.0.114
WiFiClient client;

struct MyLink *uwb_data;
int index_num = 0;
long runtime = 0;
String all_json = "";

// To display on the screen
Adafruit_SSD1306 display(128, 64, &Wire, -1);

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

    display.println("UWB tag ");
    display.display();

    //Init the Wifi

    WiFi.mode(WIFI_STA);
    WiFi.setSleep(false);
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED)
    {
        delay(500);
        Serial.print(".");
    }
    Serial.println("Connected");
    Serial.print("IP Address:");
    Serial.println(WiFi.localIP());

    if (client.connect(host, 8080))
    {
        Serial.println("Success");
        client.print(String("GET /") + " HTTP/1.1\r\n" +
                     "Host: " + host + "\r\n" +
                     "Connection: close\r\n" +
                     "\r\n");
    }

    delay(1000);

    //init the configuration
    SPI.begin(SPI_SCK, SPI_MISO, SPI_MOSI);
    DW1000Ranging.initCommunication(UWB_RST, UWB_SS, UWB_IRQ);
    DW1000Ranging.attachNewRange(newRange);
    DW1000Ranging.attachNewDevice(newDevice);
    DW1000Ranging.attachInactiveDevice(inactiveDevice);

    //we start the module as a tag
    DW1000Ranging.startAsTag(TAG_ADDR, DW1000.MODE_LONGDATA_RANGE_LOWPOWER, false);

    uwb_data = init_link();

    // print configuration
    char msgBuffer[100] = {0}; //be generous with msgBuffer size!
    DW1000Class::getPrintableDeviceMode(msgBuffer);
    Serial.println(msgBuffer);
}

int i = 0;
void loop()
{
    DW1000Ranging.loop();
    if ((millis() - runtime) > 1000) // Check every second to send data
    {
        make_link_json(uwb_data, &all_json, millis());
        send_udp(&all_json);
        runtime = millis();
        i ++;
        if (i == 30000 or i < 10)
        {
          client.connect(host, 80);
          i = 10;
        }


        // same data displayed on 128x32 OLED
        display.clearDisplay();
        display.setCursor(0, 0);
        display.print(DW1000Ranging.getDistantDevice()->getShortAddress(), HEX);
        display.print(": ");
        display.println(DW1000Ranging.getDistantDevice()->getRange(), 2);
        display.display();
    }
}

void newRange()
{
    char c[30];

    // Serial.print("from: ");
    // Serial.print(DW1000Ranging.getDistantDevice()->getShortAddress(), HEX);
    // Serial.print("\t Range: ");
    // Serial.print(DW1000Ranging.getDistantDevice()->getRange());
    // Serial.print(" m");
    // Serial.print("\t RX power: ");
    // Serial.print(DW1000Ranging.getDistantDevice()->getRXPower());
    // Serial.println(" dBm");
    // Serial.println(DW1000Ranging.getDistantDevice()->getRange());

    fresh_link(uwb_data, DW1000Ranging.getDistantDevice()->getShortAddress(), DW1000Ranging.getDistantDevice()->getRange(), DW1000Ranging.getDistantDevice()->getRXPower());
}

void newDevice(DW1000Device *device)
{
    Serial.print("ranging init; 1 device added ! -> ");
    Serial.print(" short:");
    Serial.println(device->getShortAddress(), HEX);

    add_link(uwb_data, device->getShortAddress());
}

void inactiveDevice(DW1000Device *device)
{
    Serial.print("delete inactive device: ");
    Serial.println(device->getShortAddress(), HEX);

    delete_link(uwb_data, device->getShortAddress());
}

void send_udp(String *msg_json)
{
    if (client.connected())
    {
        client.print(*msg_json);
        Serial.println("UDP send");
    }
}
void relaunch() {
  Serial.println("Relaunching device...");
  ESP.restart(); // simulate the button reset to relaunch the device
}