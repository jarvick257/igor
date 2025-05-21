#include <cstdint>
#include <string>

class RunningText {
public:
  RunningText() = default;
  RunningText(const std::string &text, uint16_t num_chars)
      : m_text{text}, m_num_chars{num_chars} {}

  std::string getAndMove() {
    if (m_text.length() <= m_num_chars)
      return m_text;

    const std::string separator = " ";
    auto text = m_text + separator + m_text;
    auto s = text.substr(m_index, m_num_chars);
    m_index = (m_index + 1) % (m_text.length() + separator.length());
    return s;
  }

  const std::string &text() { return m_text; }

private:
  std::string m_text = "";
  uint16_t m_num_chars = 16;
  uint16_t m_index = 0;
};
