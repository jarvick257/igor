class RotaryEncoder {
public:
  RotaryEncoder(int clk, int dt, int sw) : m_clk{clk}, m_dt{dt}, m_sw{sw} {}

  void init() {
    pinMode(m_clk, INPUT_PULLUP);
    pinMode(m_dt, INPUT_PULLUP);
    pinMode(m_sw, INPUT_PULLUP);
  }

  bool isButtonPressed() {
    static int last_state = HIGH;
    static unsigned long last_press = 0;

    const auto now = millis();
    if (now - last_press < m_buttonDebounceDelay)
      return false;

    int current_state = digitalRead(m_sw);
    bool pressed = current_state == LOW && last_state == HIGH;
    last_state = current_state;
    if (pressed)
      last_press = now;

    return pressed;
  }

  int getRotation() {
    static unsigned long lastRotaryTime = 0;
    static int previousCLK = digitalRead(m_clk);
    int currentCLK = digitalRead(m_clk);

    if (currentCLK == LOW && previousCLK == HIGH &&
        (millis() - lastRotaryTime > m_rotaryDebounceDelay)) {
      lastRotaryTime = millis();       // Debounce
      int DTValue = digitalRead(m_dt); // Read DT to determine direction

      previousCLK = currentCLK; // Update previous CLK for next iteration

      return (DTValue != currentCLK) ? 1 : -1; // Clockwise or counterclockwise
    }

    previousCLK = currentCLK;
    return 0; // No rotation
  }

private:
  // pins
  int m_clk, m_dt, m_sw;

  // Debounce delay
  const unsigned long m_buttonDebounceDelay = 500;

  // Faster debounce for rotary encoder
  const unsigned long m_rotaryDebounceDelay = 10;
};
