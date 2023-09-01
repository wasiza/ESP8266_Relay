
#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <ESP8266mDNS.h>

#ifndef STASSID
#define STASSID "oumta"
#define STAPSK "03269696"
#endif

const char* ssid = STASSID;
const char* password = STAPSK;

ESP8266WebServer server(80);

const int relayPin = 2; // Change this to the appropriate pin for your relay module
bool relayState = false;

void handleRoot() {
  String buttonLabel = relayState ? "Turn Off Relay" : "Turn On Relay";
  String content = "<html><head>";
  content += "<style>";
  content += "body { display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; flex-direction: column; }";
  content += "h1 { text-align: center; }";
  content += "button { margin: 10px; padding: 10px 20px; font-size: 18px; }";
  content += "</style>";
  content += "</head><body>";
  content += "<h1>Relay Control</h1>";
  content += "<form action='/toggle' method='post'>";
  content += "<button type='submit'>" + buttonLabel + "</button>";
  content += "</form>";
  content += "</body></html>";

  server.send(200, "text/html", content);
}

void handleToggle() {
  relayState = !relayState;
  digitalWrite(relayPin, relayState ? HIGH : LOW);
  Serial.println("Relay toggled: " + String(relayState));
  server.sendHeader("Location", "/");
  server.send(303);
}

void setup(void) {
  pinMode(relayPin, OUTPUT);
  digitalWrite(relayPin, LOW);

  Serial.begin(115200);
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  Serial.println("");

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  if (MDNS.begin("esp8266")) {
    Serial.println("MDNS responder started");
  }

  server.on("/", handleRoot);
  server.on("/toggle", HTTP_POST, handleToggle);

  server.begin();
  Serial.println("HTTP server started");
}

void loop(void) {
  server.handleClient();
  MDNS.update();
}
