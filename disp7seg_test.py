import RPi.GPIO as GPIO
import time
import json

# Define GPIO to REG mapping
CLK_PIN = 35

CLK_FREQ = 1
DUTY_CYCLE = 0.5

###

PERIOD = 1.0/CLK_FREQ
PULSE_H_DURATION = DUTY_CYCLE * PERIOD
PULSE_L_DURATION = (1-DUTY_CYCLE)*PERIOD

print(PERIOD, PULSE_H_DURATION, PULSE_L_DURATION)

###

def main():
  
  #GPIO.setwarnings(False)
  GPIO.setmode(GPIO.BOARD)     # use board pin numbers
  GPIO.setup(CLK_PIN, GPIO.OUT) 

  while True:

    GPIO.output(CLK_PIN, GPIO.HIGH)
    print("HIGH")
    time.sleep(PULSE_H_DURATION)
    GPIO.output(CLK_PIN, GPIO.LOW)  
    print("LOW")
    time.sleep(PULSE_L_DURATION)

    #input("Press Enter")

if __name__ == '__main__':

  #parser = argparse.ArgumentParser()
  
  #parser.add_argument("mand-arg", help="Mandatory positional argument.")
  #parser.add_argument("-c", "--char", help="Character to be displayed", required=False)
  #parser.add_argument("-b", "--opt-arg-b", help="Optional string argument, default: 3", type=int, nargs="?", default=3)
  #parser.add_argument("-c", "--opt-arg-c", help="Optional boolean argument, default: False", action="store_true", default=False)
  
  #args = parser.parse_args()

  try:
    main()
  except KeyboardInterrupt:
    pass
  finally:
    GPIO.cleanup()
