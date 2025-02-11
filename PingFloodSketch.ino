#include <ESP8266WiFi.h>
#include <ESP8266Ping.h>

const char* ssid = "vivo";  // for using my Wi-Fi SSID
const char* password = "12345678";  // for using my Wi-Fi password
IPAddress targetIP(20, 6, 129, 240);  // for using my Azure VM public IP

void setup() 
{
  Serial.begin(9600);
  WiFi.begin(ssid, password);

  // wait for connection
  while (WiFi.status() != WL_CONNECTED) 
  {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("WiFi connected");
}
void loop() 
{
  // to send ICMP ping request
  if (Ping.ping(targetIP)) 
  {
    Serial.println("Ping successful");
  } 
  else 
  {
    Serial.println("Ping failed");
  }
  delay(1000);  // Ping every second
}
