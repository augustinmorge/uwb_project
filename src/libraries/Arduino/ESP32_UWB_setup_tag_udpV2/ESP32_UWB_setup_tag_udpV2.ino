/*

For ESP32 UWB Pro with Display

*/

#include <SPI.h>
#include "DW1000Ranging.h"

#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define TAG_ADDR "7D:00:22:EA:82:60:3B:9B"

// #define DEBUG

#define SPI_SCK 18
#define SPI_MISO 19
#define SPI_MOSI 23

#define UWB_RST 27 // reset pin
#define UWB_SS 21   // spi select pin
#define UWB_IRQ 34 // irq pin

#define I2C_SDA 4
#define I2C_SCL 5

struct Link
{
    uint16_t anchor_addr;
    float range;
    float dbm;
    float fp;
    float quality;    
    struct Link *next;
};

struct Link *uwb_data;

Adafruit_SSD1306 display(128, 64, &Wire, -1);

// Constants for the Wifi
#include <WiFi.h>

// #include "link.h"
const char *ssid = "iXGuest";
const char *password = "URWelcome";
const char *host = "10.123.0.141"; //"SG_72BVTL3";
WiFiClient client;
String all_json = "";


void setup()
{
    Serial.begin(115200);

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

    logoshow();

    // init the configuration
    SPI.begin(SPI_SCK, SPI_MISO, SPI_MOSI);
    DW1000Ranging.initCommunication(UWB_RST, UWB_SS, UWB_IRQ); // Reset, CS, IRQ pin

    // DW1000.setAntennaDelay(0);

    // define the sketch as anchor. It will be great to dynamically change the type of module
    DW1000Ranging.attachNewRange(newRange);
    DW1000Ranging.attachNewDevice(newDevice);
    DW1000Ranging.attachInactiveDevice(inactiveDevice);
    // Enable the filter to smooth the distance
    // DW1000Ranging.useRangeFilter(true);

    // we start the module as a tag
    DW1000Ranging.startAsTag(TAG_ADDR, DW1000.MODE_LONGDATA_RANGE_LOWPOWER,false);
    // DW1000Ranging.startAsTag(TAG_ADDR, DW1000.MODE_SHORTDATA_FAST_LOWPOWER,false);
    // DW1000Ranging.startAsTag(TAG_ADDR, DW1000.MODE_LONGDATA_FAST_LOWPOWER,false);
    // DW1000Ranging.startAsTag(TAG_ADDR, DW1000.MODE_SHORTDATA_FAST_ACCURACY,false);
    // DW1000Ranging.startAsTag(TAG_ADDR, DW1000.MODE_LONGDATA_FAST_ACCURACY,false);
    // DW1000Ranging.startAsTag(TAG_ADDR, DW1000.MODE_LONGDATA_RANGE_ACCURACY,false);

    uwb_data = init_link();

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
}

long int runtime = 0;

void loop()
{
    DW1000Ranging.loop();
    // if ((millis() - runtime) > 1000)
    // {
        display_uwb(uwb_data);
        runtime = millis();

        // Loop for the WiFi
        make_link_json(uwb_data, &all_json, millis());
        send_udp(&all_json);
    // }
  // Serial.print(DW1000Ranging.getDistantDevice()->getRXPower());
  // Serial.print(", ");
  // Serial.print(DW1000Ranging.getDistantDevice()->getFPPower());
  // Serial.print(", diff:");
  // Serial.print(DW1000Ranging.getDistantDevice()->getRXPower() - DW1000Ranging.getDistantDevice()->getFPPower());
  // Serial.print(", ");
  // Serial.println(DW1000Ranging.getDistantDevice()->getQuality());
  // Serial.println("");
}

void newRange()
{
    // Serial.print("from: ");
    // Serial.print(DW1000Ranging.getDistantDevice()->getShortAddress(), HEX);
    // Serial.print("\t Range: ");
    // Serial.print(DW1000Ranging.getDistantDevice()->getRange());
    // Serial.print(" m");
    // Serial.print("\t RX power: ");
    // Serial.print(DW1000Ranging.getDistantDevice()->getRXPower());
    // Serial.print(" dBm");
    // Serial.print("\t FP power: ");
    // Serial.print(DW1000.getFirstPathPower());
    // Serial.print(" dBm");
    // Serial.print("\t Diff power: ");
    // Serial.print(DW1000Ranging.getDistantDevice()->getRXPower() - DW1000.getFirstPathPower());
    // Serial.print(" dBm");
    // Serial.print("\t Quality: ");
    // Serial.println(DW1000.getReceiveQuality());

    // fresh_link(uwb_data, DW1000Ranging.getDistantDevice()->getShortAddress(), DW1000Ranging.getDistantDevice()->getRange(), DW1000Ranging.getDistantDevice()->getRXPower());
    fresh_link(uwb_data, DW1000Ranging.getDistantDevice()->getShortAddress(), DW1000Ranging.getDistantDevice()->getRange(), \
                         DW1000Ranging.getDistantDevice()->getRXPower(), DW1000.getFirstPathPower(), DW1000.getReceiveQuality());

    // print_link(uwb_data);
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

// Data Link

struct Link *init_link()
{
#ifdef DEBUG
    Serial.println("init_link");
#endif
    struct Link *p = (struct Link *)malloc(sizeof(struct Link));
    p->next = NULL;
    p->anchor_addr = 0;
    p->range = 0.0;

    return p;
}

void add_link(struct Link *p, uint16_t addr)
{
#ifdef DEBUG
    Serial.println("add_link");
#endif
    struct Link *temp = p;
    // Find struct Link end
    while (temp->next != NULL)
    {
        temp = temp->next;
    }

    Serial.println("add_link:find struct Link end");
    // Create a anchor
    struct Link *a = (struct Link *)malloc(sizeof(struct Link));
    a->anchor_addr = addr;
    a->range = 0.0;
    a->dbm = 0.0;
    a->fp = 0.0;
    a->quality = 0.0;
    a->next = NULL;

    // Add anchor to end of struct Link
    temp->next = a;

    return;
}

struct Link *find_link(struct Link *p, uint16_t addr)
{
// #ifdef DEBUG
//     Serial.println("find_link");
// #endif
    if (addr == 0)
    {
        Serial.println("find_link:Input addr is 0");
        return NULL;
    }

    if (p->next == NULL)
    {
        Serial.println("find_link:Link is empty");
        return NULL;
    }

    struct Link *temp = p;
    // Find target struct Link or struct Link end
    while (temp->next != NULL)
    {
        temp = temp->next;
        if (temp->anchor_addr == addr)
        {
            // Serial.println("find_link:Find addr");
            return temp;
        }
    }

    Serial.println("find_link:Can't find addr");
    return NULL;
}

void fresh_link(struct Link *p, uint16_t addr, float range, float dbm, float fp, float quality)
{
// #ifdef DEBUG
//     Serial.println("fresh_link");
// #endif
    struct Link *temp = find_link(p, addr);
    if (temp != NULL)
    {

        temp->range = range;
        temp->dbm = dbm;
        temp->fp = fp;
        temp->quality = quality;
        return;
    }
    else
    {
        Serial.println("fresh_link:Fresh fail");
        return;
    }
}

void print_link(struct Link *p)
{
#ifdef DEBUG
    Serial.println("print_link");
#endif
    struct Link *temp = p;

    while (temp->next != NULL)
    {
        // Serial.println("Dev %d:%d m", temp->next->anchor_addr, temp->next->range);
        Serial.println(temp->next->anchor_addr, HEX);
        Serial.println(temp->next->range);
        Serial.println(temp->next->dbm);
        temp = temp->next;
    }

    return;
}

void delete_link(struct Link *p, uint16_t addr)
{
#ifdef DEBUG
    Serial.println("delete_link");
#endif
    if (addr == 0)
        return;

    struct Link *temp = p;
    while (temp->next != NULL)
    {
        if (temp->next->anchor_addr == addr)
        {
            struct Link *del = temp->next;
            temp->next = del->next;
            free(del);
            return;
        }
        temp = temp->next;
    }
    return;
}

// SSD1306

void logoshow(void)
{
    display.clearDisplay();

    display.setTextSize(2);              // Normal 1:1 pixel scale
    display.setTextColor(SSD1306_WHITE); // Draw white text
    display.setCursor(0, 0);             // Start at top-left corner
    display.println(F("Makerfabs"));

    display.setTextSize(1);
    display.setCursor(0, 20); // Start at top-left corner
    display.println(F("DW1000 DEMO"));
    display.display();
    delay(2000);
}

void display_uwb(struct Link *p)
{
    struct Link *temp = p;
    int row = 0;

    display.clearDisplay();

    display.setTextColor(SSD1306_WHITE);

    if (temp->next == NULL)
    {
        display.setTextSize(2);
        display.setCursor(0, 0);
        display.println("No Anchor");
        display.display();
        return;
    }

    while (temp->next != NULL)
    {
        temp = temp->next;

        // Serial.println("Dev %d:%d m", temp->next->anchor_addr, temp->next->range);
        // Serial.println(temp->anchor_addr, HEX);
        // Serial.println(temp->range);

        char c[30];

        // sprintf(c, "%X:%.1f m %.1f", temp->anchor_addr, temp->range, temp->dbm);
        // sprintf(c, "%X:%.1f m", temp->anchor_addr, temp->range);
        sprintf(c, "%.1f m", temp->range);
        display.setTextSize(2);
        display.setCursor(0, row++ * 32); // Start at top-left corner
        display.println(c);

        display.println("");

        sprintf(c, "%.2f dbm", temp->dbm);
        display.setTextSize(2);
        display.println(c);

        if (row >= 1)
        {
            break;
        }
    }
    delay(100);
    display.display();
    return;
}


void make_link_json(struct Link *p, String *s, long unsigned int timer)
{
#ifdef SERIAL_DEBUG
    Serial.println("make_link_json");
#endif
    *s = "{\"links\":[";
    struct Link *temp = p;

    while (temp->next != NULL)
    {
        temp = temp->next;
        // char link_json[50];
        // sprintf(link_json, "{\"A\":\"%X\",\"R\":\"%.5f\",\"T\":\"%lu\"}", temp->anchor_addr, temp->range[0], timer);
        // sprintf(link_json, "{\"A\":\"%X\",\"R\":\"%.5f\"}", temp->anchor_addr, temp->range);
        // char link_json[60];
        // sprintf(link_json, "{\"A\":\"%X\",\"R\":\"%.5f\",\"dbm\":\"%.2f\",\"T\":\"%lu\"}", temp->anchor_addr, temp->range, temp->dbm, timer);
        char link_json[120];
        sprintf(link_json, "{\"A\":\"%X\",\"R\":\"%.2f\",\"RX\":\"%.2f\",\"FP\":\"%.2f\",\"Q\":\"%.2f\",\"T\":\"%lu\"}", temp->anchor_addr, temp->range, temp->dbm, temp->fp, temp->quality, timer);
        *s += link_json;
        if (temp->next != NULL)
        {
            *s += ",";
        }
    }
    *s += "]}";
    // Serial.println(*s);
}

void send_udp(String *msg_json)
{
    if (client.connected())
    {
        client.print(*msg_json);
        // Serial.println("UDP send");
    }
    else{
      client.connect(host, 8080);
    }
}