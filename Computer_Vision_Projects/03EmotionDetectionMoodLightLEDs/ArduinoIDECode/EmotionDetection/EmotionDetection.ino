#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>

const char* ssid = "Your_Wifi_Name";             // WiFi name
const char* password = "Your_Wifi_Password";     // WiFi password

ESP8266WebServer server(80);

const int redLED = D6;
const int greenLED = D5;
const int blueLED = D7;

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);

  pinMode(redLED, OUTPUT);
  pinMode(greenLED, OUTPUT);
  pinMode(blueLED, OUTPUT);

  Serial.print("Connecting");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nConnected! IP:");
  Serial.println(WiFi.localIP());

  server.on("/emotion", []() {
    String status = server.arg("status");

    // All OFF
    digitalWrite(redLED, LOW);
    digitalWrite(greenLED, LOW);
    digitalWrite(blueLED, LOW);

    if (status == "happy") {
      digitalWrite(greenLED, HIGH);
    } else if (status == "angry") {
      digitalWrite(redLED, HIGH);
    } else {
      digitalWrite(blueLED, HIGH);
    }

    server.send(200, "text/plain", "OK");
  });

  server.begin();
}

void loop() {
  server.handleClient();
}
