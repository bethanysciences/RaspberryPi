#!/usr/bin/python
# -*- coding:utf-8 -*-
# console.py by Bob Smtih https://github.com/bethanysciences/console_rpi_epaper

import epd2in7          # https://github.com/waveshare/e-Paper
import sys
import time
import sysstats
from PIL import Image, ImageDraw, ImageFont
import RPi.GPIO as GPIO


def main():

    while(True):
        epd = epd2in7.EPD()
        epd.init()
        image = Image.new('1', (epd.width, epd.height), 255)
        draw = ImageDraw.Draw(image)
        fontDir = 'usr/share/fonts/truetype/'
        fontL = ImageFont.truetype(fontDir + 'dejavu/DejaVuSans.ttf', 22)
        fontM = ImageFont.truetype(fontDir + 'dejavu/DejaVuSans-Bold.ttf', 16)
        fontS = ImageFont.truetype(fontDir + 'dejavu/DejaVuSans.ttf', 12)

        HMargin = 2
        VMargin = 2
        tab = 5
        SpaceL = 28
        SpaceM = 20
        SpaceS = 15
        Col = HMargin
        Line = VMargin

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
        Line = Line + SpaceS

        label = "----- System Stats -----"
        w, h = fontS.getsize(label)
        draw.text(((epd.width - w) / 2, Line), label,
                  font=fontS, fill=0)
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

        image = image.transpose(Image.ROTATE_180)

        epd.display_frame(epd.get_frame_buffer(image))
        # epd.sleep()

        time.sleep(60)


if __name__ == '__main__':
    main()
