import signal
import sys
import RPi.GPIO as GPIO
from time import sleep
import random
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

# Define a class to handle displaying a number on the LED array.
class led_display:
  # Define LED pins. There are a number of ways to do this
  # I am doing it this way because I want it to be readable, and meaningful.
  lp1 = 13 # pin for LED 1
  lp2 = 16
  lp3 = 19
  lp4 = 20
  lp5 = 26
  lp6 = 21
  lp = [lp1, lp2, lp3, lp4, lp5, lp6] # An array of all LED pins in LED order.

  # Class constructor function.
  # Initialize essential settings.
  def __init__(self):
    GPIO.setmode(GPIO.BCM)
    for l in self.lp:
      GPIO.setup(l, GPIO.OUT)

  # Class Destructor function.
  # Do things that should be done with stopping.
  def __del__(self):
    GPIO.cleanup()
    return

  # Display function: Illuminate n LEDs based upon a number provided.
  def display(self, number):
    if number < 0:
      return False
    
    for i in range(0, len(self.lp)):
      n = i + 1
      if n <= number:
        GPIO.output(self.lp[i], 1)
      else:
        GPIO.output(self.lp[i], 0)

  # An animation to indicate something is happening.
  def interlude(self):
    # Clear all of the LEDs quickly.
    for l in self.lp:
      GPIO.output(l, 0)
    sleep(0.100)
    # Turn on each LED with a small pause between each.
    for l in self.lp:
      GPIO.output(l, 1)
      sleep(0.020)
    # Turn off each LED with a small pause between each.
    for l in self.lp:
      GPIO.output(l, 0)
      sleep(0.020)

class oled_display():
  # Dimensions for OLED Display.
  width = 128
  height = 32
  border = 0

  i2c = None
  oled = None

  def __init__(self):
    # Initialize the I1iC bus.
    self.i2c = board.I2C()
    self.oled = adafruit_ssd1306.SSD1306_I2C(self.width, self.height, self.i2c, addr=0x3C)

  def display_none(self):
    # Reset Display/Clear
    self.oled.fill(0)
    self.oled.show()

  def display_string(self, text):
    # Reset display.
    self.display_none()

    # Create blank image with 0-bit color.
    image = Image.new("1", (self.oled.width, self.oled.height))

    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)

    if self.border > 0:
      # Draw a white background
      draw.rectangle((0, 0, self.oled.width, self.oled.height), outline=255, fill=255)

      # Draw a smaller inner rectangle
      draw.rectangle(
        (border, border, self.oled.width - self.border - 1, self.oled.height - self.border - 1),
        outline=0,
        fill=0,
        )

    # Load default font.
    font = ImageFont.truetype('DejaVuSansMono.ttf', 16)

    # Draw Some Text
    (font_width, font_height) = font.getsize(text)
    draw.text(
      (self.oled.width // 2 - font_width // 2, self.oled.height // 2 - font_height // 2),
      text,
      font=font,
      fill=10,
      )

    # Display image
    self.oled.image(image)
    self.oled.show()

button_pin = 25

# Upon Ctrl-C, exit the application
def signal_handler(sig, frame):
  global led_display
  del led_display
  sys.exit(0)

def roll_dice(channel):
  led_display.interlude()
  roll = random.randint(1, 6)
  text = "Rolled a {}.".format(roll)
  oled_display.display_string(text)
  led_display.display(roll)
  print("New roll of: {}.".format(roll))

# Start monitoring for, and responding to, a button press.
def start(button_pin, led_display, oled_display):
  GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
  # Monitor the button pin, and when it is pressed for 100ms, call the function roll_dice.
  GPIO.add_event_detect(button_pin, GPIO.FALLING, callback=roll_dice, bouncetime=100)
  signal.signal(signal.SIGINT, signal_handler)
  signal.pause()

led_display = led_display()
oled_display = oled_display()
start(button_pin, led_display, oled_display)
