import time
import board
import terminalio
from adafruit_matrixportal.matrixportal import MatrixPortal
from secrets import secrets
import microcontroller

TEXT_COLOR = 0x202020
TIME_UPDATE_INTERVAL = 1 * 60 * 60
OPENWEATHER_API_URL = f"https://api.openweathermap.org/data/2.5/weather?q={secrets['zip']},{secrets.get('country','US')}&appid={secrets['openweather_api_key']}&units={secrets.get('units', 'imperial')}"
TEMP_PATH = ["main", "temp"]

matrixportal = MatrixPortal(
    status_neopixel=board.NEOPIXEL,
    bit_depth = 4
)

weather = None

def refresh_data():
    global weather
    temp = matrixportal.network.fetch_data(OPENWEATHER_API_URL, json_path=(TEMP_PATH))[0]
    weather = int(temp)
    matrixportal.get_local_time()

matrixportal.add_text(
    text_font=terminalio.FONT,
    text_position=(3, 9),
    text_color=TEXT_COLOR,
    text_scale=2,
)
matrixportal.add_text(
    text_font=terminalio.FONT,
    text_position=(3, 24),
    text_color=TEXT_COLOR,
)

matrixportal.set_text("Connecting", 1)
matrixportal.network.connect()
matrixportal.set_text("Get time", 1)
# matrixportal.get_local_time()
refresh_data()

last_time_refresh = time.time()

epoch = 1584576000 #march 19, 2020 00:00 UTC
seconds_per_day = 24 * 60 * 60

days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

matrixportal.preload_font(b"012345789Quarantinedy")  # preload numbers
try:
    while True: 
        t = time.time()
        dt = time.localtime(t)
        hour = dt.tm_hour
        if hour == 0: hour = 12
        elif hour > 12: hour -= 12
        first_line = f"{hour:02}:{(dt.tm_min):02}"
        day_of_week = days[dt.tm_wday]
        date = ""
        data_selector = t % 90
        if data_selector >= 60:
            day = (t - epoch) // seconds_per_day
            date = f"QD {day}"
        elif data_selector >= 30:
            date = f"{weather}F"
        else:
            date = f"{dt.tm_mon:02}/{dt.tm_mday:02}"
        matrixportal.set_text(first_line, 0)
        matrixportal.set_text(f"{day_of_week} {date}", 1)
        if (t - last_time_refresh > TIME_UPDATE_INTERVAL):
            refresh_data()
            # matrixportal.get_local_time()
            last_time_refresh = t
        time.sleep(0.05)
except e:
    microcontroller.reset()