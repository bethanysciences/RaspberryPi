#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys
import time
import sysstats
from PIL import Image, ImageDraw, ImageFont
import epd2in7
import RPi.GPIO as GPIO

epd = epd2in7.EPD()
epd.init()
fontL = ImageFont.truetype('lib/Font.ttc', 24)
fontM = ImageFont.truetype('lib/Font.ttc', 18)
fontS = ImageFont.truetype('lib/Font.ttc', 12)


def sysDisplay():
    HMargin = 2
    VMargin = 2
    tab = 5
    SpaceL = 28
    SpaceM = 20
    SpaceS = 14
    Col = HMargin
    Line = VMargin

    screen = Image.new('1', (epd.width, epd.height), 255)
    draw = ImageDraw.Draw(screen)

    host = "%s" % sysstats.GetHost()
    w, h = fontL.getsize(host)
    draw.text(((epd.width - w) / 2, Line), host, font=fontL, fill=0)
    Line = Line + SpaceL

    ipAddress = "%s" % sysstats.GetIPAddress()
    w, h = fontM.getsize(ipAddress)
    draw.text(((epd.width - w) / 2, Line), ipAddress, font=fontM, fill=0)
    Line = Line + SpaceM

    CurrTime = "%s" % sysstats.GetCurrTime()
    w, h = fontM.getsize(CurrTime)
    draw.text(((epd.width - w) / 2, Line), CurrTime, font=fontM, fill=0)
    Line = Line + SpaceM

    label = "----- System Stats -----"
    w, h = fontS.getsize(label)
    draw.text(((epd.width - w) / 2, Line), label, font=fontS, fill=0)
    Line = Line + SpaceS

    draw.text((Col, Line), "temp %s" % sysstats.GetCPUTemp(),
              font=fontS, fill=0)
    Line = Line + SpaceS

    draw.text((Col, Line), "up %s" % sysstats.GetUpTime(),
              font=fontS, fill=0)
    Line = Line + SpaceS

    draw.text((Col, Line), "utilization %s" % sysstats.GetCPUUtilization(),
              font=fontS, fill=0)
    Line = Line + SpaceS

    label = "----- Network Stats -----"
    w, h = fontS.getsize(label)
    draw.text(((epd.width - w) / 2, Line), label, font=fontS, fill=0)
    Line = Line + SpaceS

    draw.text((Col, Line), 'ssid: %s'
              % sysstats.GetSSID('wlan0'), font=fontS, fill=0)
    Line = Line + SpaceS

    draw.text((Col, Line), 'frequency: %s'
              % sysstats.GetFrequency('wlan0'), font=fontS, fill=0)
    Line = Line + SpaceS

    draw.text((Col, Line), 'bit rate: %s'
              % sysstats.GetBitRate('wlan0'), font=fontS, fill=0)
    Line = Line + SpaceS

    draw.text((Col, Line), 'link quality: %s'
              % sysstats.GetLinkQuality('wlan0'), font=fontS, fill=0)
    Line = Line + SpaceS

    draw.text((Col, Line), 'signal level: %s'
              % sysstats.SignalQuality('wlan0'), font=fontS, fill=0)
    Line = Line + SpaceS

    draw.text((Col, Line), 'traffic tx: %s rx: %s'
              % sysstats.GetNetworkUsage('wlan0'), font=fontS, fill=0)

    epd.display_frame(epd.get_frame_buffer(screen))


while True:
    sysDisplay()
    time.sleep(60)
