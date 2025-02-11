#include <ESP8266WiFi.h>
#include <ESP8266Ping.h>

const char* ssid     = "vivo";     
const char* password = "12345678";

IPAddress targetIP(20, 6, 129, 240);  

unsigned long pingInterval = 10;  

void setup() {
  Serial.begin(115200);
  
  WiFi.begin(ssid, password);
  Serial.print("Connecting to Wi-Fi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnected to Wi-Fi");

  if (Ping.ping(targetIP)) {
    Serial.println("Ping successful!");
  } else {
    Serial.println("Ping failed.");
  }
}

void loop() {
  bool result = Ping.ping(targetIP);
  
  if (result) {
    Serial.println("Ping sent successfully");
  } else {
    Serial.println("Ping failed");
  }
  delay(pingInterval);
}
