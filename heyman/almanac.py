from datetime import datetime, date, time, timezone
import schedule
import pandas as pd
from suntime import Sun, SunTimeException
from adafruit_ht16k33 import segments
import board
import busio

# Setup display hardware
i2c = busio.I2C(board.SCL, board.SDA)
clockDisplay = segments.Seg7x4(i2c, address=0x70)  # white
highDisplay = segments.Seg7x4(i2c, address=0x77)   # blue
lowDisplay = segments.Seg7x4(i2c, address=0x72)    # blue
setDisplay = segments.Seg7x4(i2c, address=0x74)    # red
riseDisplay = segments.Seg7x4(i2c, address=0x73)   # red


def clock():
    dt = datetime.now()
    clock = '%02d:%02d' % (dt.hour, dt.minute)

    clockDisplay.print(clock)
    if dt.second % 2:
        clockDisplay.print(':')
    else:
        clockDisplay.print(';')

    # print(clock)


def tides():
    dt = datetime.now()
    dtf = datetime.strftime(dt, "%Y%m%d")

    address = "https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?"
    date = "begin_date=" + dtf + "&range=36"
    # station = "8558690" # INDIAN RIVER INLET, DE
    station = "8726724"  # Clearwater Beach, FL
    product = "predictions"
    datum = "mllw"
    units = "english"
    time_zone = "lst_ldt"
    interval = "hilo"
    application = "web_services"
    type = "csv"

    url = (address + date +
           "&station=" + station +
           "&product=" + product +
           "&datum=" + datum +
           "&units=" + units +
           "&time_zone=" + time_zone +
           "&interval=" + interval +
           "&application=" + application +
           "&format=" + type)

    # print(url)

    df = pd.read_csv(url)

    # print(df.head(10))

    df['Date Time'] = pd.to_datetime(df['Date Time'])
    mask = (df['Date Time'] > datetime.now())
    df = df.loc[mask]

    # print(df.head(10))

    if df.iloc[0, 2] == "L":
        lowTime = df.iloc[0, 0]
        lowLevel = df.iloc[0, 1]

        highTime = df.iloc[1, 0]
        highLevel = df.iloc[1, 1]

    else:
        highTime = df.iloc[0, 0]
        highLevel = df.iloc[0, 1]

        lowTime = df.iloc[1, 0]
        lowLevel = df.iloc[1, 1]

    highDisplay.print(highTime.strftime("%H:%M"))
    lowDisplay.print(lowTime.strftime("%H:%M"))

    print("High Tide", highTime.strftime("%H:%M"),
          "level", round(highLevel, 1),
          "ft. | Low Tide", lowTime.strftime("%H:%M"),
          "level", round(lowLevel, 1), "ft.")


def sunriset():
    latitude = 27.97    # Clearwater Beach, FL
    longitude = -82.83  # Clearwater Beach, FL
    # latitude = 38.61    # Bethany Beach, DE
    # longitude = -75.07  # Bethany Beach, DE
    sun = Sun(latitude, longitude)
    riseTime = sun.get_local_sunrise_time()
    setTime = sun.get_local_sunset_time()

    setDisplay.print(setTime.strftime("%H:%M"))
    riseDisplay.print(riseTime.strftime("%H:%M"))

    # print("Sunrise", riseTime.strftime("%H:%M"),
    #       " | Sunset", setTime.strftime("%H:%M"))


clock()
tides()
sunriset()

schedule.every(1).seconds.do(clock)
schedule.every().day.at("00:30").do(sunriset)
schedule.every(3).hours.do(tides)

while True:
    schedule.run_pending()
