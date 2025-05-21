#include <Adafruit_SSD1306.h>
#include <Wire.h>
#include <string>

#include "RunningText.h"

class Display {
public:
  Display() {
    m_display = Adafruit_SSD1306(m_width, m_height, &Wire, D4);
    this->update("Title", "Subtitle");
  }

  void update(const std::string &title, const std::string &body) {
    if (title != m_title.text()) {
      m_title = RunningText(title, m_width / textWidth(m_title_font_size));
    }
    if (body != m_body.text()) {
      m_body = RunningText(body, m_width / textWidth(m_body_font_size));
    }
    m_last_step = 0;
  }

  void init() {
    if (!m_display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
      Serial.println(F("SSD1306 allocation failed"));
      for (;;)
        ;
    }
    m_display.clearDisplay();
    Serial.println("Display initialized.");
  }

  void show() {
    const auto now = millis();
    if ((now - m_last_step) < m_ms_per_step)
      return;
    m_last_step = now;

    m_display.setTextColor(WHITE);
    m_display.clearDisplay();

    printRow(0, m_title.getAndMove(), m_title_font_size);
    printRow(1, m_body.getAndMove(), m_body_font_size);

    m_display.display(); // Show the updated display
  }

  void successAnimation(String text = "SUCCESS!") {
    m_display.clearDisplay();
    int centerX = 64, centerY = 32;

    for (int radius = 2; radius <= 30; radius += 2) {
      m_display.drawCircle(centerX, centerY, radius, WHITE);
      m_display.display();
      delay(100);

      if (radius % 4 == 0) {
        m_display.clearDisplay();
        m_display.display();
        delay(2);
      }
    }

    m_display.clearDisplay();
    m_display.setTextSize(2);
    m_display.setCursor(20, 20);
    m_display.print(text);
    m_display.display();
    delay(1000);
    m_display.clearDisplay();
    m_display.display();
  }

private:
  static constexpr uint16_t textWidth(uint16_t font_size, uint16_t chars = 1) {
    return chars * font_size * 6;
  }

  void printRow(int row, std::string text, uint16_t font_size) {
    int text_width = textWidth(font_size, text.length());
    int x = (m_width - text_width) / 2; // Center the text on the top row
    x = std::max(x, 0);
    m_display.setTextSize(font_size);     // Larger size for top row
    m_display.setCursor(x, row * 35); // Centered on top row
    m_display.print(text.c_str());
  }

  RunningText m_title;
  RunningText m_body;

  static constexpr uint16_t m_width = 128;
  static constexpr uint16_t m_height = 64;
  static constexpr uint16_t m_title_font_size = 2;
  static constexpr uint16_t m_body_font_size = 2;

  uint32_t m_last_step = 0;
  uint32_t m_current_display_index = 0;
  const uint32_t m_ms_per_step = 300;

  Adafruit_SSD1306 m_display;
};
