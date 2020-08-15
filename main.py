from mod_seven_segment_board import *
from mod_nunchuck import nunchuck
from mod_led_matrix_board import *
from mod_halt_button import *

import time
import datetime
import sys

ssb = SevenSegmentBoard()
ssb.set_text("")
ssb.start()

lmb = LEDMatrixBoard()

btn = HaltButton()

#wii = nunchuck()

try:
  while True:
    #if not wii.button_c() and not wii.button_z():
    #  time.sleep(0.1)
    #elif wii.button_c() and not wii.button_z():
    #  ssb.set_text("{:04d}{:04d}".format(wii.joystick_x(), wii.joystick_y()))
    #  #time.sleep(0.1)
    #elif not wii.button_c() and wii.button_z():
    #  lmb.display_string_scroll("text", persistence=0.08)
    #else:
    #  time.sleep(0.1)
    #ssb.display_text("{0:%H%M%d%m}".format(datetime.datetime.now()), persistence=5)
    ssb.display_text("{0:%H%M}".format(datetime.datetime.now()), persistence=1)
    #ssb.display_text("{0:%d%m}".format(datetime.datetime.now()), persistence=3)
    #lmb.display_string_scroll("ITEAC", persistence=0.08)
    if btn.pressed():
      print("HaltButton")
      sys.exit(5)
except KeyboardInterrupt:
  print("KeyboardInterrupt")
  pass
finally:
  print("Cleanup")
  ssb.cleanup()
  ssb.join()
  lmb.cleanup()
  GPIO.cleanup()
