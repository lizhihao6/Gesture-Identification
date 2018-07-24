# -*- coding: utf-8 -*-
#!/usr/bin/env python

# Ported from:
# https://github.com/adafruit/Adafruit_Python_SSD1306/blob/master/examples/shapes.py

from oled.device import ssd1306, sh1106
from oled.render import canvas
from PIL import ImageFont, ImageDraw, Image


class OLED:


    def __init__(self):
        
        try:
            # self.font = ImageFont.load_default()
            self.font = ImageFont.truetype("/root/oled/font/arial.ttf",16)
            self.device = sh1106(port=1, address=0x3C)
            self.draw_text("OLED INIT")

        except:
            with open("error.txt","a+") as file:
                file.write("Failed to init OLED\n")


    def draw_text(self, text):

        with canvas(self.device) as draw:

            padding = 4
            top = padding
            lines = text.split("\n")
            for line in lines:
                draw.text( (padding, top + lines.index(line)*19), line, font=self.font, fill=255)
    

    def draw_image(self, path, bias):

        with canvas(self.device) as draw:

            img = Image.open(path)
            draw.bitmap((bias, 0), img, fill=1)


if __name__ == "__main__":

    oled = OLED()