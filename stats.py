#!/usr/bin/python3
# V1 20210313 - changed shell command to get system load
# prerequisites:
# sudo pip3 install adafruit-circuitpython-lis3dh
# sudo pip3 install adafruit-circuitpython-ssd1306
# forked from https://github.com/adafruit/Adafruit_CircuitPython_SSD1306/blob/master/examples/ssd1306_stats.py
import time
import subprocess

from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

i2c = busio.I2C(SCL, SDA)

disp = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

disp.fill(0)
disp.show()

width = disp.width
height = disp.height

image = Image.new("1", (width, height))
draw = ImageDraw.Draw(image)
font = ImageFont.load_default()

while True:
    cmd = "hostname -I | cut -d\' \' -f1"
    IP = subprocess.check_output(cmd, shell = True ).decode('utf-8')
    ''' the folowing line fails to display proper information on systems where comma is used instead of dot as decimal separator
    cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
    '''
    cmd = "cut -f 1 -d \" \" /proc/loadavg"
    CPU = subprocess.check_output(cmd, shell = True ).decode('utf-8')
    cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
    MemUsage = subprocess.check_output(cmd, shell = True ).decode('utf-8')
    cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
    Disk = subprocess.check_output(cmd, shell = True ).decode('utf-8')
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    draw.text((0, -2), "IP: " + IP, font=font, fill=255)
    draw.text((0, 6), "CPU load: " + CPU, font=font, fill=255)
    draw.text((0, 14), MemUsage, font=font, fill=255)
    draw.text((0, 23), Disk, font=font, fill=255)

    disp.image(image)
    disp.show()
    time.sleep(1)
