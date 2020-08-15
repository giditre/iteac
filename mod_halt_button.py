import RPi.GPIO as GPIO

import time

class HaltButton():

  def __init__(self, btn_pin=40, pud=GPIO.PUD_DOWN):
    self.btn_pin = btn_pin

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(btn_pin, GPIO.IN, pull_up_down=pud)

  def pressed(self):
    if GPIO.input(self.btn_pin):
      while GPIO.input(self.btn_pin):
        time.sleep(0.01)
      return True
    else:
      return False

if __name__ == "__main__":

  btn = HaltButton()

  try:
    while True:

      if btn.pressed():
        print("Pressed!")

      time.sleep(0.01)

  except KeyboardInterrupt:
    pass
  finally:
    GPIO.cleanup()
