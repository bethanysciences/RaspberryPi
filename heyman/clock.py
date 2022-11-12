from datetime import datetime, date, time, timezone
import schedule
from adafruit_ht16k33 import segments
import board
import busio

# Setup display hardware
i2c = busio.I2C(board.SCL, board.SDA)
clockDisplay = segments.Seg7x4(i2c, address=0x70)  # white


def clock():
    dt = datetime.now()
    clock = '%02d:%02d' % (dt.hour, dt.minute)

    clockDisplay.print(clock)
    if dt.second % 2:
        clockDisplay.print(':')
    else:
        clockDisplay.print(';')

    print(clock)


clock()

schedule.every(1).seconds.do(clock)

while True:
    schedule.run_pending()
