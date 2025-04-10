#include <Wire.h>
#include <Adafruit_SSD1306.h>
#include <ArduinoJson.h>

#include "ESP8266WiFi.h"
#include "ESP8266mDNS.h"
#include "EspMQTTClient.h"
#include "LEAmDNS.h"
#include "PubSubClient.h"
#include "secrets.h"

#define DEVICE_NAME "zigor/client"

#define CLK    D6
#define DT     D7
#define SW     D4

Adafruit_SSD1306 display(128, 64, &Wire, D4);
EspMQTTClient client(WIFI_SSID, WIFI_PSK, BROKER_IP, DEVICE_NAME);

const unsigned long buttonDebounceDelay = 500;  // Debounce delay
const unsigned long rotaryDebounceDelay = 10;  // Faster debounce for rotary encoder

void printDisplayRow(int row, String text, int size=-1){
  const int width = 128;
  int chars = text.length();

  if(size == -1){
    float pixel_per_char = (float)width / chars;
    float max_text_size = pixel_per_char / 6.0;
    size = int(max_text_size + 0.5) - 1;
    size = size < 1 ? 1 : size;
  }

  int textWidth = chars * size * 6;  // TextSize 2, so 12 pixels per char
  int x = (width - textWidth) / 2;  // Center the text on the top row
  display.setTextSize(size);  // Larger size for top row
  display.setCursor(x, row * 30);  // Centered on top row
  display.print(text);
}

// Update the OLED display with the current state
void updateDisplay(String title, String body) {
  display.setTextColor(WHITE);
  display.clearDisplay();

  printDisplayRow(0, title, 2);
  printDisplayRow(1, body);

  display.display();  // Show the updated display
}

// Detect button presses with debounce logic
bool buttonPressed() {
  static int last_state = HIGH;
  static unsigned long last_press = 0;

  const auto now = millis();
  if(now - last_press < buttonDebounceDelay) return false;

  int current_state = digitalRead(SW);
  bool pressed = current_state == LOW && last_state == HIGH;
  last_state = current_state;
  if(pressed) last_press = now;

  return pressed;
}

// Success animation when a session ends
void successAnimation(String text="SUCCESS!") {
  display.clearDisplay();
  int centerX = 64, centerY = 32;

  for (int radius = 2; radius <= 30; radius += 2) {
    display.drawCircle(centerX, centerY, radius, WHITE);
    display.display();
    delay(100);

    if (radius % 4 == 0) {
      display.clearDisplay();
      display.display();
      delay(2);
    }
  }

  display.clearDisplay();
  display.setTextSize(2);
  display.setCursor(20, 20);
  display.print(text);
  display.display();
  delay(1000);
  display.clearDisplay();
  display.display();
}

// Rotary Encoder Rotation Detection
int getRotation() {
  static unsigned long lastRotaryTime = 0;
  static int previousCLK = digitalRead(CLK);
  int currentCLK = digitalRead(CLK);

  if (currentCLK == LOW && previousCLK == HIGH && (millis() - lastRotaryTime > rotaryDebounceDelay)) {
    lastRotaryTime = millis();  // Debounce
    int DTValue = digitalRead(DT);  // Read DT to determine direction

    previousCLK = currentCLK;  // Update previous CLK for next iteration

    return (DTValue != currentCLK) ? 1 : -1;  // Clockwise or counterclockwise
  }

  previousCLK = currentCLK;
  return 0;  // No rotation
}

// Handle rotary input for menu and countdown selection
void handleRotaryInput() {
  auto rotation = getRotation();
  auto button_pressed = buttonPressed();

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
    updateDisplay(doc["title"], doc["body"]);
  });
}

void setup() {
  pinMode(CLK, INPUT_PULLUP);
  pinMode(DT, INPUT_PULLUP);
  pinMode(SW, INPUT_PULLUP);
  Serial.begin(9600);

  initDisplay();
  updateDisplay("IGOR", "Welcome");
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
    successAnimation("I.G.O.R.");
    was_connected = true;
  }

  // Handle rotary encoder input
  handleRotaryInput();
}

void initDisplay() {
  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println(F("SSD1306 allocation failed"));
    for (;;);
  }
  display.clearDisplay();
  Serial.println("Display initialized.");
}

