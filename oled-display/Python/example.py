import board
import busio
import adafruit_ssd1306

# Initialize the I2C bus
I2C = busio.I2C(board.IO9, board.IO8)

# Initialize the OLED display
display = adafruit_ssd1306.SSD1306_I2C(128, 64, I2C)

# Display a message
while True:
    display.fill_rect(0, 0, 128, 10, 0)
    text = str("Hello World!")
    display.text(text, 0, 0, 1)
    display.show()
