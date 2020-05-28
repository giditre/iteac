import pigpio
import time

# BOARD 31 - BCM 6
A_neg = 6
# BOARD 33 - BCM 13
A_pos = 13

pi = pigpio.pi() # connect to local Pi

pi.set_mode(A_neg, pigpio.OUTPUT)
pi.set_mode(A_pos, pigpio.OUTPUT)

pi.write(A_neg, 0)
pi.write(A_pos, 0)



try:
  while True:
    pi.set_PWM_dutycycle(A_pos, 200) # PWM 1/2 on
    time.sleep(0.2)
    pi.set_PWM_dutycycle(A_pos, 0) # PWM off
    pi.set_PWM_dutycycle(A_neg, 200) # PWM off
    time.sleep(0.2)
    pi.set_PWM_dutycycle(A_neg, 0) # PWM off

except KeyboardInterrupt:
  pass

pi.set_PWM_dutycycle(A_pos, 0) # PWM off
pi.set_PWM_dutycycle(A_neg, 0) # PWM off

pi.write(A_neg, 0)
pi.write(A_pos, 0)

pi.stop()

