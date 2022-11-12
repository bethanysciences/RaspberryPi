from datetime import datetime, date, time, timezone
from suntime import Sun, SunTimeException
from adafruit_ht16k33 import segments
import board
import busio


# Setup display hardware
i2c = busio.I2C(board.SCL, board.SDA)
setDisplay = segments.Seg7x4(i2c, address=0x74)    # red
riseDisplay = segments.Seg7x4(i2c, address=0x73)   # red


def sunriset():
    latitude = 38.61
    longitude = -75.07
    sun = Sun(latitude, longitude)
    riseTime = sun.get_local_sunrise_time()
    setTime = sun.get_local_sunset_time()

    setDisplay.print(setTime.strftime("%H:%M"))
    riseDisplay.print(riseTime.strftime("%H:%M"))

    print("Sunrise", riseTime.strftime("%H:%M"),
          " | Sunset", setTime.strftime("%H:%M"))


sunriset()
