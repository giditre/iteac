import pigpio
import time

import gpio_utils as gu

class DCMotor():

  def __init__(self, A_neg_pin = 36, A_pos_pin = 38, PWM_duty = 255):

    self.A_neg = gu.board_to_bcm(A_neg_pin)
    self.A_pos = gu.board_to_bcm(A_pos_pin)

    self.pi = pigpio.pi() # connect to local Pi

    self.pi.set_mode(self.A_neg, pigpio.OUTPUT)
    self.pi.set_mode(self.A_pos, pigpio.OUTPUT)

    self.pi.write(self.A_neg, 0)
    self.pi.write(self.A_pos, 0)

    self.PWM_duty = PWM_duty

  def move_forward(self, duration=0.1):
    self.pi.set_PWM_dutycycle(self.A_pos, self.PWM_duty) # PWM on
    time.sleep(duration)
    self.pi.set_PWM_dutycycle(self.A_pos, 0) # PWM off

  def move_backward(self, duration=0.2):
    self.pi.set_PWM_dutycycle(self.A_neg, self.PWM_duty) # PWM on
    time.sleep(duration)
    self.pi.set_PWM_dutycycle(self.A_neg, 0) # PWM off

  def wiggle(self, semiperiod=0.1):
    for i in range(3):
      self.move_forward(semiperiod)
      self.move_backward(semiperiod)

  def cleanup(self):
    self.pi.set_PWM_dutycycle(self.A_pos, 0) # PWM off
    self.pi.set_PWM_dutycycle(self.A_neg, 0) # PWM off
    self.pi.write(self.A_neg, 0)
    self.pi.write(self.A_pos, 0)
    self.pi.stop()

if __name__ == "__main__":

  dcm = DCMotor()

  try:

    dcm.wiggle()

  except KeyboardInterrupt:
    pass

  dcm.cleanup()
