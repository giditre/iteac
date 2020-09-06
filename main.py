from mod_seven_segment_board import *
from mod_nunchuck import nunchuck
from mod_led_matrix_board import *
from mod_halt_button import *
from mod_floppy import *
from mod_lcd import *
from mod_buzzer import *
from mod_dc_motor import *

import time
import datetime
import sys

ssb = SevenSegmentBoard()
ssb.set_text("")
ssb.start()

lmb = LEDMatrixBoard()

lcd = LCD()

fdr = FloppyDrive()

dcm = DCMotor()

bzr = Buzzer()

btn = HaltButton()

wii = nunchuck()

modes = ["Demo", "7 Segment Board", "LED Matrix", "Buzzer", "Presence sensor", "Floppy Music", "Printer Cart"]

mode_i = 0

try:

  while True:

    if wii.button_z():
      tmp_mode_i = mode_i
      lcd.lcd_text("{:16}{:16}".format("Select mode:", modes[tmp_mode_i]))
      while wii.button_z():
        j_dir = wii.jooystick_direction()
        if j_dir == "R":
          if tmp_mode_i > 0:
            tmp_mode_i -= 1
            lcd.lcd_text("{:16}{:16}".format("Select mode:", modes[tmp_mode_i]))
        elif j_dir == "L":
          if tmp_mode_i < len(modes)-2:
            tmp_mode_i += 1
            lcd.lcd_text("{:16}{:16}".format("Select mode:", modes[tmp_mode_i]))
      mode_i = tmp_mode_i

    if mode_i == 0:
      now = datetime.datetime.now()

      #ssb.display_text("{0:%H%M%d%m}".format(datetime.datetime.now()), persistence=5)
      ssb.display_text("{0:%H%M}".format(now), persistence=3)
      ssb.display_text("    {0:%d%m}".format(datetime.datetime.now()), persistence=3)

      lmb.display_string_scroll("{0:%A}".format(now), persistence=0.08)

      lcd.lcd_text("{1:16}{0:%a} {0:%b} {0:%d} {0:%Y}".format(now, "Today's date:"))
      lcd.clear()

      for i in range(3):
        bzr.beep(0.1)
        time.sleep(0.1)

      fdr.play_wave("tonelist_imperialmarch_short.json")

      dcm.wiggle(0.3)

    else:
      lcd.lcd_text("{:16}{:16}".format(modes[tmp_mode_i], "not implemented"))

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
  fdr.cleanup()
  dcm.cleanup()
  GPIO.cleanup()
