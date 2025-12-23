#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>

const char* ssid = "Your_Wifi_Name";
const char* password = "Your_Wifi_Password";

ESP8266WebServer server(80);

const int greenLED = D5;

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);

  pinMode(greenLED, OUTPUT);

  Serial.print("Connecting");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nConnected! IP:");
  Serial.println(WiFi.localIP());

  server.on("/qr", []() {
    String state = server.arg("state");
    if (state == "1") {
      digitalWrite(greenLED, HIGH);
    } else {
      digitalWrite(greenLED, LOW);
    }
    server.send(200, "text/plain", "QR LED status updated");
  });

  server.begin();
}

void loop() {
  server.handleClient();
}
