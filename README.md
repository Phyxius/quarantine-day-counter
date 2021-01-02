# Quarantine Day Counter

This is a simple internet-connected clock/quarantine day counter. It uses an [Adafruit Matrix Portal](https://www.adafruit.com/product/4745) to display text on an [appropriate 64x32 RGB LED matrix](https://www.adafruit.com/product/2279). Power can be supplied over USB-C or an external power supply.

## Installation

1. Flash the Matrix Portal to run CircuitPython using Adafruit's instructions. 
2. Install the libraries in [`required_libraries.txt`](required_libraries.txt).
3. Configure [`secrets.py`](secrets.py) with the appropriate WiFi credentials, time zone, and Adafruit.IO credentials.
4. Finally, overwrite `code.py` with the code from this repository.