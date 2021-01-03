import time
import board
import terminalio
from adafruit_matrixportal.matrixportal import MatrixPortal
from secrets import secrets

TEXT_COLOR = 0x202020
TIME_UPDATE_INTERVAL = 12 * 60 * 60

matrixportal = MatrixPortal(
    status_neopixel=board.NEOPIXEL,
    bit_depth = 4
)

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
matrixportal.get_local_time()

last_time_refresh = time.time()

epoch = 1584576000 #march 19, 2020 00:00 UTC
seconds_per_day = 24 * 60 * 60

days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
# months = ['Jan', 'Feb', 'March', 'Apr', 'May', 'June', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

matrixportal.preload_font(b"012345789Quarantinedy")  # preload numbers
while True: 
    t = time.time()
    dt = time.localtime(t)
    hour = dt.tm_hour
    if hour == 0: hour = 12
    elif hour > 12: hour -= 12
    first_line = f"{hour:02}:{(dt.tm_min):02}"
    day_of_week = days[dt.tm_wday]
    date = ""
    if t % 60 >= 30:
        day = (t - epoch) // seconds_per_day
        date = f"QD {day}"
    else:
        date = f"{dt.tm_mday:02}/{dt.tm_mon:02}"
    matrixportal.set_text(first_line, 0)
    matrixportal.set_text(f"{day_of_week} {date}", 1)
    if (t - last_time_refresh > TIME_UPDATE_INTERVAL):
        matrixportal.get_local_time()
        last_time_refresh = t
    time.sleep(0.05)