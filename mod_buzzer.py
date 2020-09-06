import RPi.GPIO as GPIO

import time

class Buzzer():

  def __init__(self, buzz_pin=7):
    self.buzz_pin = buzz_pin

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(buzz_pin, GPIO.OUT, initial=GPIO.LOW)

  def beep(self, duration=1):
    GPIO.output(self.buzz_pin, GPIO.HIGH)
    time.sleep(duration)
    GPIO.output(self.buzz_pin, GPIO.LOW)

  def cleanup(self):
    GPIO.cleanup()

if __name__ == "__main__":

  bzr = Buzzer()

  try:
    while True:
      bzr.beep()
      time.sleep(1)

  except KeyboardInterrupt:
    pass
  finally:
    bzr.cleanup()
