import RPi.GPIO as GPIO
import time
import argparse
import json

relays = {
  1: 32,
  2: 36,
  3: 38,
  4: 40
}

RELAY_ON = GPIO.LOW
RELAY_OFF = GPIO.HIGH

def main(*args, **kwargs):

  relay_n = 0
  if "relay_n" in kwargs:
    relay_n = kwargs["relay_n"]

  GPIO.setmode(GPIO.BOARD)     # use board pin numbers

  for i in range(1, 4+1):
    GPIO.setup(relays[i], GPIO.OUT)
    GPIO.output(relays[i], RELAY_OFF)

  if relay_n > 0:
    input("Press Enter to switch RELAY{} on...".format(relay_n))
    GPIO.output(relays[relay_n] , RELAY_ON)
    input("Press Enter to switch RELAY{} off...".format(relay_n))
    GPIO.output(relays[relay_n] , RELAY_OFF)
  else:
    for i in range(1, 4+1):
      input("Press Enter to switch RELAY{} on...".format(i))
      GPIO.output(relays[i] , RELAY_ON)
      input("Press Enter to switch RELAY{} off...".format(i))
      GPIO.output(relays[i] , RELAY_OFF)

  input("Press Enter to quit...")

if __name__ == '__main__':

  parser = argparse.ArgumentParser()
  parser.add_argument("relay", help="Relay number", type=int)
  args = parser.parse_args()

  relay_n = args.relay
    
  try:
    main(relay_n=relay_n)
  except KeyboardInterrupt:
    pass
  finally:
    for i in range(1, 4+1):
      GPIO.output(relays[i], RELAY_OFF)
    GPIO.cleanup()
