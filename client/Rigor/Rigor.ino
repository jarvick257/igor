#include <Wire.h>
#include <Adafruit_SSD1306.h>
#include <ArduinoJson.h>

#include "ESP8266WiFi.h"
#include "ESP8266mDNS.h"
#include "EspMQTTClient.h"
#include "LEAmDNS.h"
#include "PubSubClient.h"
#include "Secrets.h"
#include "Display.h"
#include "RotaryEncoder.h"

#define DEVICE_NAME "rigor/client"

#define CLK    D6
#define DT     D7
#define SW     D4

Display display{};
RotaryEncoder encoder{CLK, DT, SW};
EspMQTTClient mqtt(WIFI_SSID, WIFI_PSK, BROKER_IP, DEVICE_NAME);

void handleRotaryInput() {
  auto rotation = encoder.getRotation();
  auto button_pressed = encoder.isButtonPressed();

  const char* action = nullptr;
  if (button_pressed)     action = "ENTER";
  else if (rotation ==-1) action = "PREV";
  else if (rotation == 1) action = "NEXT";

  if(action == nullptr) return;
  mqtt.publish("rigor/input", String(action), false);
  Serial.print("Published ");
  Serial.println(String(action));
}

void onConnectionEstablished() {
  Serial.println("MQTT Connected");
  mqtt.subscribe("rigor/screen", [](const String &payload) {
    Serial.print("Screen: ");
    Serial.println(String(payload));

    JsonDocument doc;
    deserializeJson(doc, payload);
    display.update(doc["title"], doc["body"]);
  });
}

void setup() {
  encoder.init();
  Serial.begin(9600);

  display.init();
  display.update("RIGOR", "Welcome");
  display.show();
  Serial.println("Setup complete, starting loop...");
  mqtt.setKeepAlive(60);
}

void loop() {
  static bool was_connected = false;
  mqtt.loop();

  if (false == mqtt.isMqttConnected()) {
    display.update("RIGOR", "Connecting");
    display.show();
    delay(100);
    return;
  }

  if(!was_connected){
    display.update("RIGOR", "Welcome");
    display.show();
    delay(1000);
    was_connected = true;
  }

  // Handle rotary encoder input
  handleRotaryInput();
  display.show();
}
