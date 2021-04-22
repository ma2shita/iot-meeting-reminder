#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os


import logging
import epd2in7
import time
from PIL import Image,ImageDraw,ImageFont

logging.basicConfig(level=logging.DEBUG)

def show(event):
    try:
        epd = epd2in7.EPD()
        
        '''2Gray(Black and white) display'''
        logging.info("init and Clear")
        
        epd.init()
        epd.Clear(0xFF)
        Himage = Image.new('1', (epd.height, epd.width), 255)
        if(event != 'No Event'):
            bmp = Image.open('event.bmp')
        else:
            bmp = Image.open('NoEvent.bmp')
        Himage.paste(bmp)
        epd.display(epd.getbuffer(Himage))
        time.sleep(2)


    except IOError as e:
        logging.info(e)
        
    except KeyboardInterrupt:    
        logging.info("ctrl + c:")
        epd2in7.epdconfig.module_exit()
        exit()
