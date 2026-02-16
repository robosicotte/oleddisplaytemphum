"""
oleddisplaytemphum
By Matthew Sicotte

Uses an SSD1306 OLED to display current temperature and humidity, from a CSV file.

"""
import board
import digitalio
from PIL import Image, ImageDraw, ImageFont

import adafruit_ssd1306
from datetime import datetime
import signal
import time
from argparse import ArgumentParser
from pathlib import Path
import pandas as pd
from enum import Enum
from temphumdata import temphumdata
from boundingboxutils import *

DEFAULT_DISPLAY_ADDR=0x3D
DEFAULT_FONT_SIZE=24
DEFAULT_Y_PADDING=8
DEFAULT_X_PADDING=8
DEFAULT_TIME_ON=5
DEFAULT_LOG_FILE='/home/pi/pythonprog/oleddisplaytemphum/logfile.txt'
i2c = board.I2C()  

button=digitalio.DigitalInOut(board.D21)
button.direction=digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP
        
def append_log_file(logfilename, msg):
    with open(logfilename, 'a') as fp:
        fp.write(f'{datetime.now()}: {msg}\n')

def poweroff(sig, frame):
    print('Powering off OLED.')
    display.poweroff()
    exit(0)

signal.signal(signal.SIGINT, poweroff)

def read_curr_temp_hum(filename):
    df=pd.read_csv(filename, index_col=False, parse_dates=['time_local'])
    currtempdata=df.iloc[0]
    return temphumdata(currtempdata['time_local'], currtempdata['temp'], currtempdata['humidity'])


def parse_args():
    """
    parse_args: Parses args and returns them
    Returns:
    args (argparse.namespace): The args parsed.
    """
    parser=ArgumentParser()
    parser.add_argument('--fontsize', '-S', type=float, default=DEFAULT_FONT_SIZE, help=f'Font size in pixels; default {DEFAULT_FONT_SIZE}')
    parser.add_argument('--displayaddr', '-A', type=int, default=DEFAULT_DISPLAY_ADDR, help=f'Display address; default {DEFAULT_DISPLAY_ADDR}')
    parser.add_argument('--filename', '-f', type=str, default='/home/pi/pythonprog/temphumlogger/datafiles/currtemphum.csv', help='Temp and Hum file name.')
    parser.add_argument('--timeon', '-t', type=float, default=DEFAULT_TIME_ON, help=f'Time on in seconds; default {DEFAULT_TIME_ON}')
    parser.add_argument('--centerx', action='store_true', help='Center x.')
    parser.add_argument('--centery', action='store_true', help='Center y.')
    parser.add_argument('--ypadding', type=int, default=DEFAULT_Y_PADDING, help=f'Y padding; default {DEFAULT_Y_PADDING}')
    parser.add_argument('--xpadding', type=int, default=DEFAULT_X_PADDING, help=f'X padding; default {DEFAULT_X_PADDING}; overwritten by centerx')
    parser.add_argument('--logfile', '-L', type=str, default=DEFAULT_LOG_FILE, help=f'Log file name; default {DEFAULT_LOG_FILE}')
    parser.add_argument('--continuous', '-c', action='store_true', help='Continuous mode')
    args=parser.parse_args()
    return args

def display_temp_hum(display, currtemphum, font, args):
    temp_f_str=f'{currtemphum.get_temp_f()} F'
    hum_str=f'{currtemphum.get_humidity()} %'
    temp_f_str_bbox=TextBoundingBox(font.getbbox(temp_f_str))
    hum_str_bbox=TextBoundingBox(font.getbbox(hum_str))
    temphumtextimg=Image.new('1', (display.width, display.height))
    temphumtextimg_draw=ImageDraw.Draw(temphumtextimg)
    ypadding=args.ypadding
    xpadding=args.xpadding
    temp_xc, temp_yc=temp_f_str_bbox.get_center()
    temp_ybottom=temp_f_str_bbox.get_ybottom()+ypadding
    hum_ytop=temp_ybottom+ypadding
    temp_offset_x=max(round(display.width/2-temp_xc), 0)
    hum_xc, hum_yc=hum_str_bbox.get_center()
    hum_offset_x=max(round(display.width/2-hum_xc), 0)

    #First center x if necessary (assume no center y)
    if args.centerx:
        tempxy=[temp_offset_x, ypadding]
        humxy=[hum_offset_x, hum_ytop]
    else:
        #No center x
        tempxy=[xpadding, ypadding]
        humxy=[xpadding, hum_ytop]
    #Now center y if necessary:
    if args.centery:
        ytotal=temp_f_str_bbox.get_height()+hum_str_bbox.get_height()+ypadding
        yoffset=max(display.height/2-ytotal/2, 0)
        tempxy[1]=yoffset
        humxy[1]=tempxy[1]+temp_f_str_bbox.get_height()+ypadding

    temphumtextimg_draw.text(tempxy, temp_f_str, font=font, fill=255)
    temphumtextimg_draw.text(humxy, hum_str, font=font, fill=255)
    display.image(temphumtextimg)
    display.show()

def main():
    args=parse_args()
    fontsize=args.fontsize
    global display #Declare global display to turn off on signal.
    display=adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=args.displayaddr)
    font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSans.ttf", fontsize)
    if args.continuous:
        while True:
            while button.value == 1:
                pass
            try:
                currtemphum=read_curr_temp_hum(args.filename)
                log_str=f'Reading curr temp h/hum success'
                append_log_file(args.logfile, log_str)
            except Exception as e:
                exception_msg_str=f'Exception while reading curr temp file: {e}'
                print(exception_msg_str)
                append_log_file(args.logfile, exception_msg_str)
            try:
                display.poweron()
                display_temp_hum(display, currtemphum, font, args)
                append_log_file(args.logfile, 'Display temp hum success')
            except Exception as e:
                exception_msg_str=f'Exception while displaying curr temp/hum: {e}'
                print(exception_msg_str)
                append_log_file(args.logfile, exception_msg_str)
            time.sleep(args.timeon)
            try:
                display.poweroff()
            except Exception as e:
                exception_msg_str=f'Exception while powering off display: {e}'
                print(exception_msg_str)
                append_log_file(args.logfile, exception_msg_str)
    else:
        while button.value == 1:
            pass
        currtemphum=read_curr_temp_hum(args.filename)
        display.poweron()
        display_temp_hum(display, currtemphum, font, args)
        time.sleep(args.timeon)
    display.poweroff()

if __name__ == '__main__':
    main()