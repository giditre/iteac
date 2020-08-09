import time
from mod_seven_segment_board import *
from mod_nunchuck import nunchuck
from mod_led_matrix_board import *

wii = nunchuck()

ssb = SevenSegmentBoard()
ssb.set_text("")
ssb.start()

lmb = LEDMatrixBoard()

try:
  while True:
    if not wii.button_c() and not wii.button_z():
      time.sleep(0.1)
    elif wii.button_c() and not wii.button_z():
      ssb.set_text("{:04d}{:04d}".format(wii.joystick_x(), wii.joystick_y()))
      #time.sleep(0.1)
    elif not wii.button_c() and wii.button_z():
      lmb.display_string_scroll("text", persistence=0.08)
    else:
      time.sleep(0.1)
except KeyboardInterrupt:
  ssb.cleanup()
  ssb.join()
  lmb.cleanup()
  GPIO.cleanup()
