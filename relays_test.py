import RPi.GPIO as GPIO
import time
import argparse
import json

relays = {
  1: 40,
  2: 38,
  3: 36,
  4: 32
} 

RELAY_ON = GPIO.LOW
RELAY_OFF = GPIO.HIGH

def main():
  
  GPIO.setmode(GPIO.BOARD)     # use board pin numbers

  for i in range(1, 4+1):
    GPIO.setup(relays[i], GPIO.OUT)
    GPIO.output(relays[i], RELAY_OFF)

  for i in range(1, 4+1):
    input("Press Enter to switch RELAY{} on...".format(i))
    GPIO.output(relays[i] , RELAY_ON)
    input("Press Enter to switch RELAY{} off...".format(i))
    GPIO.output(relays[i] , RELAY_OFF)
    
  input("Press Enter to quit...")

if __name__ == '__main__':

  try:
    main()
  except KeyboardInterrupt:
    pass
  finally:
    for i in range(1, 4+1):
      GPIO.output(relays[i], RELAY_OFF)
    GPIO.cleanup()
