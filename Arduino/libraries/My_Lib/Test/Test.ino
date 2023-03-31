#include <WiFi.h>
#include <WiFiUDP.h>

const char* ssid = "iXGuest";
const char* password = "URWelcome";
const char* host = "SG_72BVTL3";

WiFiUDP udp;

void setup() {
  Serial.begin(115200);
  delay(1000);

  // Connect to Wi-Fi network
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");

  // Perform DNS lookup to get IP address of host
  Serial.print("Performing DNS lookup for host: ");
  Serial.println(host);
  udp.beginPacket("8.8.8.8", 53);
  byte dns_header[] = {0x00, 0x00, // Identifier
                       0x01, 0x00, // Flags
                       0x00, 0x01, // Questions
                       0x00, 0x00, // Answer RRs
                       0x00, 0x00, // Authority RRs
                       0x00, 0x00  // Additional RRs
  };
  udp.write(dns_header, sizeof(dns_header));
  int hostname_len = strlen(host);
  for (int i = 0; i < hostname_len; i++) {
    if (host[i] == '.') {
      udp.write(i - 1);
      for (int j = i - 1; j >= 0; j--) {
        udp.write(host[j]);
      }
      host += i;
      hostname_len -= i;
      i = -1;
    }
  }
  udp.write(hostname_len - 1);
  for (int i = hostname_len - 1; i >= 0; i--) {
    udp.write(host[i]);
  }
  udp.write((byte)0);
  udp.write((byte)0);
  udp.write((byte)0x01);
  udp.write((byte)0x00);
  udp.write((byte)0x01);
  udp.endPacket();

  while (udp.parsePacket() <= 0) {
    delay(100);
    Serial.println("Waiting for DNS response...");
  }

  byte ip[4];
  udp.read(ip, sizeof(ip));
  char ip_str[16];
  sprintf(ip_str, "%d.%d.%d.%d", ip[0], ip[1], ip[2], ip[3]);
  Serial.print("Resolved IP address: ");
  Serial.println(ip_str);
  
  // Connect to host on port 8080
  Serial.print("Connecting to host: ");
  Serial.println(ip_str);
  WiFiClient client;
  if (client.connect(ip_str, 8080)) {
    Serial.println("Connected to host");
    client.println("GET / HTTP/1.1");
    client.println("Host: " + String(host));
    client.println("Connection: close");
    client.println();
  }
  else {
    Serial.println("Connection to host failed");
  }
}

void loop() {
  // do nothing
}
