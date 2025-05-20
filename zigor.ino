#include <Wire.h>
#include <Adafruit_SSD1306.h>
#include <ArduinoJson.h>

#include "ESP8266WiFi.h"
#include "ESP8266mDNS.h"
#include "EspMQTTClient.h"
#include "LEAmDNS.h"
#include "PubSubClient.h"
#include "secrets.h"
#include "Display.h"
#include "RotaryEncoder.h"

#define DEVICE_NAME "zigor/client"

#define CLK    D6
#define DT     D7
#define SW     D4

Display display{};
RotaryEncoder encoder{CLK, DT, SW};
EspMQTTClient client(WIFI_SSID, WIFI_PSK, BROKER_IP, DEVICE_NAME);

void handleRotaryInput() {
  auto rotation = encoder.getRotation();
  auto button_pressed = encoder.isButtonPressed();

  const char* action = nullptr;
  if (button_pressed)     action = "ENTER";
  else if (rotation ==-1) action = "PREV";
  else if (rotation == 1) action = "NEXT";

  if(action == nullptr) return;
  client.publish("zigor/input", String(action), false);
  Serial.print("Published ");
  Serial.println(String(action));
}

void onConnectionEstablished() {
  Serial.println("MQTT Connected");
  client.subscribe("zigor/screen", [](const String &payload) {
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
  display.update("IGOR", "Welcome");
  Serial.println("Setup complete, starting loop...");
  client.setKeepAlive(60);
}

void loop() {
  static bool was_connected = false;
  client.loop();

  if (false == client.isMqttConnected()) {
    Serial.println("Waiting for connection...");
    delay(500);
    return;
  }

  if(!was_connected){
    display.successAnimation("I.G.O.R.");
    was_connected = true;
  }

  // Handle rotary encoder input
  handleRotaryInput();
  display.show();
}


