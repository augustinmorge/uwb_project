//anchor #4 setup


// be sure to edit tag_addr and select the previously calibrated anchor delay
// my naming convention is anchors 1, 2, 3, ... have the lowest order byte of the MAC address set to 81, 82, 83, ...

#include <SPI.h>
#include "DW1000Ranging.h"
// #include "DW1000.h"
// 
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

int selected_anchor = 80;
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

struct Link
{
    uint16_t tag_addr;
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
const char *host = "10.123.0.186"; //"SG_72BVTL3";
WiFiClient client;
String all_json = "";


void starting_parameters(){
  switch(selected_anchor){
    case 80:
      anchorAddress = "80:17:5B:D5:A9:9A:E2:9C";
      anchorAddress.toCharArray(ANCHOR_ADD, 24);
      // Adelay = 16520;
      // Adelay = 16535;
      Adelay = 16529.41;
      str_display =  "UWB Anchor 80 ";
      break;
    case 81:
      anchorAddress = "81:17:5B:D5:A9:9A:E2:9C";
      anchorAddress.toCharArray(ANCHOR_ADD, 24);
      // Adelay = 16539;
      // Adelay = 16550;
      Adelay = 16535.48;
      str_display =  "UWB Anchor 81 ";
      break;
    case 82:
      anchorAddress = "82:17:5B:D5:A9:9A:E2:9C";
      anchorAddress.toCharArray(ANCHOR_ADD, 24);
      // Adelay = 16445;
      Adelay = 16550; //16549.71;
      str_display =  "UWB Anchor 82 ";
      break;
    case 83:
      anchorAddress = "83:17:5B:D5:A9:9A:E2:9C";
      anchorAddress.toCharArray(ANCHOR_ADD, 24);
      // Adelay = 16505;
      // Adelay = 16540;
      Adelay = 16533; //16532.50;
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

  // // set antenna delay for anchors only. Tag is default (16384)
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

// const byte DW1000Class::MODE_LONGDATA_RANGE_LOWPOWER[] = {TRX_RATE_110KBPS, TX_PULSE_FREQ_16MHZ, TX_PREAMBLE_LEN_2048};
// const byte DW1000Class::MODE_SHORTDATA_FAST_LOWPOWER[] = {TRX_RATE_6800KBPS, TX_PULSE_FREQ_16MHZ, TX_PREAMBLE_LEN_128};
// const byte DW1000Class::MODE_LONGDATA_FAST_LOWPOWER[]  = {TRX_RATE_6800KBPS, TX_PULSE_FREQ_16MHZ, TX_PREAMBLE_LEN_1024};
// const byte DW1000Class::MODE_SHORTDATA_FAST_ACCURACY[] = {TRX_RATE_6800KBPS, TX_PULSE_FREQ_64MHZ, TX_PREAMBLE_LEN_128};
// const byte DW1000Class::MODE_LONGDATA_FAST_ACCURACY[]  = {TRX_RATE_6800KBPS, TX_PULSE_FREQ_64MHZ, TX_PREAMBLE_LEN_1024};
// const byte DW1000Class::MODE_LONGDATA_RANGE_ACCURACY[] = {TRX_RATE_110KBPS, TX_PULSE_FREQ_64MHZ, TX_PREAMBLE_LEN_2048};

long int runtime = 0;

void loop()
{
  DW1000Ranging.loop();
  if ((millis() - runtime) > 1000)
    {
        display_uwb(uwb_data);
        runtime = millis();

        // Loop for the WiFi
        make_link_json(uwb_data, &all_json, millis());
        send_udp(&all_json);
    }
}

void newRange()
{
    Serial.println("\nNew values:");
    Serial.println(DW1000Ranging.getDistantDevice()->getRange());
    Serial.println(DW1000Ranging.getDistantDevice()->getShortAddress());
    Serial.println(DW1000Ranging.getDistantDevice()->getRXPower());
    Serial.println(DW1000Ranging.getDistantDevice()->getFPPower());
    Serial.println(DW1000Ranging.getDistantDevice()->getQuality());
    // print_link(uwb_data);
    fresh_link(uwb_data, DW1000Ranging.getDistantDevice()->getShortAddress(), DW1000Ranging.getDistantDevice()->getRange(), \
                         DW1000Ranging.getDistantDevice()->getRXPower(), DW1000Ranging.getDistantDevice()->getFPPower(), DW1000Ranging.getDistantDevice()->getQuality()); 

}

void newDevice(DW1000Device *device)
{
    Serial.print("Device added: ");
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
    p->tag_addr = 0;
    p->range = 0.0;
    p->dbm = 0.0;
    p->fp = 0.0;
    p->quality = 0.0;

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
    // Create a tag
    struct Link *a = (struct Link *)malloc(sizeof(struct Link));
    a->tag_addr = addr;
    a->range = 0.0;
    a->dbm = 0.0;
    a->fp = 0.0;
    a->quality = 0.0;
    a->next = NULL;

    // Add tag to end of struct Link
    temp->next = a;

    return;
}

struct Link *find_link(struct Link *p, uint16_t addr)
{
#ifdef DEBUG
    Serial.println("find_link");
#endif
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
        if (temp->tag_addr == addr)
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
#ifdef DEBUG
    Serial.println("fresh_link");
#endif
    struct Link *temp = find_link(p, addr);
    if (temp != NULL)
    {

        temp->range = range;
        temp->dbm = dbm;
        temp->fp = fp;
        temp->quality = quality;

        // Serial.println(range);
        // Serial.println(dbm);

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
        // Serial.println("Dev %d:%d m", temp->next->tag_addr, temp->next->range);
        Serial.println(temp->next->tag_addr, HEX);
        Serial.println(temp->next->range);
        Serial.println(temp->next->dbm);
        Serial.println(temp->next->fp);
        Serial.println(temp->next->quality);
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
        if (temp->next->tag_addr == addr)
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

        // Serial.println("Dev %d:%d m", temp->next->tag_addr, temp->next->range);
        // Serial.println(temp->tag_addr, HEX);
        // Serial.println(temp->range);

        char c[30];

        // sprintf(c, "%X:%.1f m %.1f", temp->tag_addr, temp->range, temp->dbm);
        // sprintf(c, "%X:%.1f m", temp->tag_addr, temp->range);
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
        // sprintf(link_json, "{\"A\":\"%X\",\"R\":\"%.5f\",\"T\":\"%lu\"}", temp->tag_addr, temp->range[0], timer);
        // sprintf(link_json, "{\"A\":\"%X\",\"R\":\"%.5f\"}", temp->tag_addr, temp->range);
        // char link_json[60];
        // sprintf(link_json, "{\"A\":\"%X\",\"R\":\"%.5f\",\"dbm\":\"%.2f\",\"T\":\"%lu\"}", temp->tag_addr, temp->range, temp->dbm, timer);
        char link_json[120];
        sprintf(link_json, "{\"A\":\"%X\",\"R\":\"%.3f\",\"RX\":\"%.3f\",\"FP\":\"%.3f\",\"Q\":\"%.3f\",\"T\":\"%lu\"}", temp->tag_addr, temp->range, temp->dbm, temp->fp, temp->quality, timer);
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