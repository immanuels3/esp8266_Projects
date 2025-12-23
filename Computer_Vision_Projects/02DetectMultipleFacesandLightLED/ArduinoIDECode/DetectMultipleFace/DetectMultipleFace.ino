#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>

const char* ssid = "Your_Wifi_Name";            // 🔁 WiFi Name
const char* password = "Your_Wifi_Password";    // 🔁 WiFi Password

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

  server.on("/face", []() {
    String status = server.arg("status");

    // Turn OFF all first
    digitalWrite(redLED, LOW);
    digitalWrite(greenLED, LOW);
    digitalWrite(blueLED, LOW);

    if (status == "0") {
      digitalWrite(redLED, HIGH);
    } else if (status == "1") {
      digitalWrite(greenLED, HIGH);
    } else if (status == "2") {
      digitalWrite(blueLED, HIGH);
    }

    server.send(200, "text/plain", "OK");
  });

  server.begin();
}

void loop() {
  server.handleClient();
}
