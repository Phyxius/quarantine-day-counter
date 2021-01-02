import time
import board
import terminalio
from adafruit_matrixportal.matrixportal import MatrixPortal
from secrets import secrets


matrixportal = MatrixPortal(
    status_neopixel=board.NEOPIXEL,
)

matrixportal.add_text(
    text_font=terminalio.FONT,
    text_position=(1, 6),
    text_color=0x505050,
)

matrixportal.set_text("Connecting\nto WiFi...")
matrixportal.network.connect()
matrixportal.set_text("Getting\ntime...")
matrixportal.get_local_time()

last_time_refresh = time.time()

epoch = 1584576000 #march 19, 2020 00:00 UTC
seconds_per_day = 24 * 60 * 60

days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
# months = ['Jan', 'Feb', 'March', 'Apr', 'May', 'June', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

matrixportal.preload_font(b"012345789Quarantinedy")  # preload numbers
while True: 
    t = time.time()
    if t % 60 >= 30:
        day = (t - epoch) // seconds_per_day
        matrixportal.set_text(f"Quarantine\nday {day}")
    else:
        dt = time.localtime(t)
        hour = dt.tm_hour
        if hour == 0: hour = 12
        elif hour > 12: hour -= 12
        ampm = 'PM' if dt.tm_hour >=12 else 'AM'
        matrixportal.set_text(f"{hour:02}:{(dt.tm_min):02} {ampm}\n{days[dt.tm_wday]} {dt.tm_mday:02}/{dt.tm_mon:02}")
    time.sleep(0.05)