# -*- coding: utf-8 -*-
# Leonardo Lazzaro @ 2017-09-10
import os
import time
from datetime import datetime
from multiprocessing import Process

from pygpio import SPI
from char_lcd.pcd8544 import (
    PCD8544,
    LCDWIDTH,
    LCDHEIGHT
)

from PIL import Image, ImageDraw, ImageFont

# Raspberry Pi hardware SPI config:
ON = 1
DC = 23
RST = 24
LED = 18
OFF = 0
OUT = 0
SPI_PORT = 1
SPI_DEVICE = 0


class LCDMonitor(Process):

    def __init__(self, redis):
        super(LCDMonitor, self).__init__()
        self.redis = redis
        # Hardware SPI usage:
        self.disp = PCD8544(DC, RST, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=4000000))
        # Initialize library.
        self.disp.begin(contrast=60)
        # Load default font.
        font_filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'DroidSansMono.ttf')
        self.small_font = ImageFont.truetype(font_filename, 7)
        self.big_font = ImageFont.truetype(font_filename, 20)
        self.font = ImageFont.load_default()
        self.disp._gpio.setup(LED, OUT)
        # Clear display.
        self.disp.clear()
        self.disp.display()
        self.light_on()

    def show_message(self, message):
        image = Image.new('1', (LCDWIDTH, LCDHEIGHT))
        draw = ImageDraw.Draw(image)
        draw.text((10, 10), message, font=self.font)
        self.disp.image(image)
        self.disp.display()

    def run(self):
        self.light_on()
        while True:
            try:
                position = self.redis.hgetall('position')
                interfaces = self.redis.lrange('interfaces', 0, -1)
                session_stats = self.redis.hgetall('session_stats')
                self.draw_stats(position, interfaces, session_stats)
                time.sleep(0.5)
            except KeyboardInterrupt:
                self.show_message('Stopped')
                self.light_off()
                self.disp.reset()
                break

    def draw_stats(self, position, interfaces, session_stats):
        # Create blank image for drawing.
        # Make sure to create image with mode '1' for 1-bit color.
        image = Image.new('1', (LCDWIDTH, LCDHEIGHT))

        # Get drawing object to draw on image.
        draw = ImageDraw.Draw(image)

        # Draw a white filled box to clear the image.
        draw.rectangle((0, 0, LCDWIDTH, LCDHEIGHT), outline=255, fill=255)

        # Alternatively load a TTF font.
        # Some nice fonts to try: http://www.dafont.com/bitmap.php
        # font = ImageFont.truetype('Minecraftia.ttf', 8)

        # Write some text.
        if position:
            gps_status = '1'
        else:
            gps_status = '0'
        load_avg = os.getloadavg()
        satellites = self.redis.get('satellites')
        draw.text((0, 0), 'I{0} GPS {1} SAT{2} L{3}'.format(len(interfaces), gps_status, satellites, load_avg[0]), font=self.small_font)
        draw.text((0, 6), '4W {0} ATK {1}'.format(session_stats['4way'], session_stats['attack_count']), font=self.font)
        draw.text((0, 14), 'OPN {0} BT {1}'.format(session_stats['open'], session_stats['bt']), font=self.font)
        draw.text((0, 22), 'WEP {0} NRF {1}'.format(session_stats['wep'], session_stats['nrf24']), font=self.font)
        draw.text((0, 30), 'WPA/WPA2 {0}'.format(int(session_stats['wpa']) + int(session_stats['wpa2']) + int(session_stats['wpa2 wpa'])), font=self.font)
        draw.text((0, 38), '{0}'.format(datetime.now().strftime("%H:%M:%S")), font=self.font)

        # Display image.
        self.disp.image(image)
        self.disp.display()

    def light_on(self):
        self.set_brightness(1)

    def light_off(self):
       self.set_brightness(0)

    def set_brightness(self, led_value):
        if (0 <= led_value < 1023):
            self.disp._gpio.output(LED, led_value)
        else:
            if led_value == 0:
                self.disp._gpio.output(LED, OFF)
            else:
                self.disp._gpio.output(LED, ON)

if __name__ == '__main__':
    from redis import StrictRedis
    redis_server = StrictRedis('localhost', decode_responses=True, charset="utf-8")

    redis_server.hset('session_stats', '4way', 1)
    redis_server.hset('session_stats', 'bt', 2)
    redis_server.hset('session_stats', 'open', 3)
    redis_server.hset('session_stats', 'wep', 4)
    redis_server.hset('session_stats', 'wpa', 5)
    redis_server.hset('session_stats', 'wpa2', 6)
    redis_server.hset('session_stats', 'wpa2 wpa', 7)
    redis_server.hset('session_stats', 'attack_count', 8)
    lcd=LCDMonitor(redis_server)
    lcd.start()
