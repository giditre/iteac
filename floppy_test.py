import RPi.GPIO as GPIO
import time

STEP = 31
DIR = 29
WRITE = 33

DIR_FWD = GPIO.LOW
DIR_BCK = GPIO.HIGH

SLEEP = 0.004

N_ST_FWD = 10
N_ST_BCK = 10

N_ST_RESET = 80

###

POSITION = 0
DIRECTION = DIR_FWD

###

GPIO.setmode(GPIO.BOARD)

GPIO.setup(STEP, GPIO.OUT) # Step (Floppy Pin 20)
GPIO.setup(DIR, GPIO.OUT) # Direction (Floppy Pin 18)
GPIO.setup(WRITE, GPIO.OUT) # Write (Floppy Pin 22)

def reset_position():
  global POSITION
  # reset variable
  position = 0
  # move the head the maximum amount of steps back
  GPIO.output(DIR, DIR_BCK)
  for s in range(N_ST_RESET+1):
    # send one step pulse
    GPIO.output(STEP, GPIO.HIGH)
    time.sleep(0.005)
    GPIO.output(STEP, GPIO.LOW)
    time.sleep(0.005)

def step(steps, period=0.01):
  global POSITION
  global DIRECTION
  
  print(POSITION, DIRECTION)

  # convert period to float
  period = float(period)
  
  # adjust direction based on global POSITION
  # start by keeping current direction
  # set direction pin
  GPIO.output(DIR, DIRECTION)

  remaining_steps = steps
  while remaining_steps:
    # send one step pulse
    GPIO.output(STEP, GPIO.HIGH)
    time.sleep(period/2)
    GPIO.output(STEP, GPIO.LOW)
    time.sleep(period/2)
    # decrement residual steps counter
    remaining_steps -= 1
    # update position
    POSITION = POSITION+1 if DIRECTION == DIR_FWD else POSITION-1
    # avoid making more steps than POSITION allows
    # invert DIRECTION if reached limit
    if POSITION == 0:
      DIRECTION = DIR_FWD
      GPIO.output(DIR, DIR_FWD)
    elif POSITION == 80:
      DIRECTION = DIR_BCK
      GPIO.output(DIR, DIR_BCK)
    print(POSITION, DIRECTION)

def tone(freq, duration):
  # how many periods in 1 second of a 100Hz tone? 100.
  # how many periods in 2 seconds of a 100Hz tone? 200.
  # how many in 3 seconds? 300. So...
  steps = int(freq * duration)

  period = 1.0/freq

  step(steps, period)

def main():

  # reset head position
  reset_position()

  #step(1000, 0.005)

  t1 = time.time()
  tone(400, 2)
  t2 = time.time()
  print("Duration: {}".format(t2-t1))

if __name__ == "__main__":
  try:
    main()
  except KeyboardInterrupt:
    print("Cleaning up...")
    GPIO.cleanup()

