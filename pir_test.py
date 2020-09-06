import RPi.GPIO as GPIO
import time

PIR_PIN = 35

GPIO.setmode(GPIO.BOARD)

#Read output from PIR motion sensor
GPIO.setup(PIR_PIN, GPIO.IN)

while True:
  if GPIO.input(PIR_PIN):
    print("Chi siete?")
    t = 0
    while GPIO.input(PIR_PIN):
      print(".", end='', flush=True)
      t += 1
      time.sleep(0.1)
    print("Un fiorino!")
    print(t)
  time.sleep(0.1)

