# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
# SPDX-License-Identifier: MIT

# This example is for use on (Linux) computers that are using CPython with
# Adafruit Blinka to support CircuitPython libraries. CircuitPython does
# not support PIL/pillow (python imaging library)!
#
# Ported to Pillow by Melissa LeBlanc-Williams for Adafruit Industries from Code available at:
# https://learn.adafruit.com/adafruit-oled-displays-for-raspberry-pi/programming-your-display

#Modified version of script by Matthew Sicotte

#NOTE that the displayio SSD1306 libraries do not seem to work well on Pi 5;
#A workaround is to use the adafruit-circuitpython-ssd1306 libraries


import board
import digitalio
from PIL import Image, ImageDraw, ImageFont

import adafruit_ssd1306
import time
import signal
import time
i2c = board.I2C()  

# Create the SSD1306 OLED class.
# The first two parameters are the pixel width and pixel height.
# Change these to the right size for your display!
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3D)
def poweroff(sig, frame):
    print('Powering off OLED.')
    oled.poweroff()
    exit(0)

signal.signal(signal.SIGINT, poweroff)
def main():
    # Clear display.
    oled.fill(0)
    oled.show()

    # Create blank image for drawing.

    # Load a font in 2 different sizes.
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 28)
    font2 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)

    # Draw the text
    for idx in range(10):
        image = Image.new("1", (oled.width, oled.height))
        draw = ImageDraw.Draw(image)

        draw.text((0, 0), "Hello!", font=font, fill=255)
        draw.text((0, 30), f"{idx}", font=font2, fill=255)
        #draw.text((34, 46), "Hello!", font=font2, fill=255)

        # Display image
        oled.image(image)
        oled.show()
        time.sleep(2)
    oled.poweroff()

if __name__ == '__main__':
    main()