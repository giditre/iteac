from seven_segment_board import *
from nunchuck import nunchuck

wii = nunchuck()
ssb = SevenSegmentBoard()

try:
  while True:
    ssb.display_text("{:04d}{:04d}".format(wii.joystick_x(), wii.joystick_y()), persistence=0.1)
except KeyboardInterrupt:
  ssb.cleanup()
  GPIO.cleanup()
