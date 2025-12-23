#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>

const char* ssid = "Your_Wifi_Name";          // 🔁 WiFi பெயர்
const char* password = "Your_Wifi_Password";  // 🔁 WiFi கடவுச்சொல்

ESP8266WebServer server(80);

const int redLED = D6;
const int greenLED = D5;

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  
  pinMode(redLED, OUTPUT);
  pinMode(greenLED, OUTPUT);

  Serial.print("Connecting");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nConnected! IP:");
  Serial.println(WiFi.localIP());

  server.on("/face", []() {
    String status = server.arg("status");
    if (status == "1") {
      digitalWrite(greenLED, HIGH);
      digitalWrite(redLED, LOW);
    } else {
      digitalWrite(greenLED, LOW);
      digitalWrite(redLED, HIGH);
    }
    server.send(200, "text/plain", "OK");
  });

  server.begin();
}

void loop() {
  server.handleClient();
}
