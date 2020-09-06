import pigpio
import time

import gpio_utils as gu

A_neg = 36
A_pos = 38

A_neg = gu.board_to_bcm(A_neg)
A_pos = gu.board_to_bcm(A_pos)

pi = pigpio.pi() # connect to local Pi

pi.set_mode(A_neg, pigpio.OUTPUT)
pi.set_mode(A_pos, pigpio.OUTPUT)

pi.write(A_neg, 0)
pi.write(A_pos, 0)

try:

  for i in range(3):
    PWM_duty = 255
    print(PWM_duty)
    pi.set_PWM_dutycycle(A_pos, PWM_duty) # PWM on
    time.sleep(0.5)
    pi.set_PWM_dutycycle(A_pos, 0) # PWM off
    pi.set_PWM_dutycycle(A_neg, PWM_duty) # PWM off
    time.sleep(0.5)
    pi.set_PWM_dutycycle(A_neg, 0) # PWM off

except KeyboardInterrupt:
  pass

pi.set_PWM_dutycycle(A_pos, 0) # PWM off
pi.set_PWM_dutycycle(A_neg, 0) # PWM off

pi.write(A_neg, 0)
pi.write(A_pos, 0)

pi.stop()

