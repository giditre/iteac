import pigpio
import time

# BOARD 31 - BCM 6
A_neg = 6
# BOARD 33 - BCM 13
A_pos = 13
# BOARD 35 - BCM 19
B_neg = 19
# BOARD 37 - BCM 26
B_pos = 26

pi = pigpio.pi() # connect to local Pi

pi.set_mode(A_neg, pigpio.OUTPUT)
pi.set_mode(A_pos, pigpio.OUTPUT)
pi.set_mode(B_neg, pigpio.OUTPUT)
pi.set_mode(B_pos, pigpio.OUTPUT)

pi.write(A_neg, 0)
pi.write(A_pos, 0)
pi.write(B_neg, 0)
pi.write(B_pos, 0)

pi.wave_clear()

#coil_list = [

# clockwise
pulse_list = ['0100', '0110', '0010', '1010', '1000', '1001', '0001', '0101']
# counterclockwise
#pulse_list = ['0100', '0101', '0001', '1001', '1000', '1010', '0010', '0110']

pulse_period_us = 10000
pulse_period = float(pulse_period_us)/1e6

try:
  while True:
    for p in range(len(pulse_list)-1):
      pulse = pulse_list[p]
      next_pulse = pulse_list[p+1]

      print(pulse, next_pulse)  

      pi.write(A_neg, int(pulse[0]))
      pi.write(A_pos, int(pulse[1]))
      pi.write(B_neg, int(pulse[2]))
      pi.write(B_pos, int(pulse[3]))
      time.sleep(pulse_period)
      
      pi.write(A_neg, int(next_pulse[0]))
      pi.write(A_pos, int(next_pulse[1]))
      pi.write(B_neg, int(next_pulse[2]))
      pi.write(B_pos, int(next_pulse[3]))
      time.sleep(pulse_period)

      pi.write(A_neg, 0)
      pi.write(A_pos, 0)
      pi.write(B_neg, 0)
      pi.write(B_pos, 0)

      input("Press Enter")

      #time.sleep(0.1)
except KeyboardInterrupt:
  pass

pi.write(A_neg, 0)
pi.write(A_pos, 0)
pi.write(B_neg, 0)
pi.write(B_pos, 0)

pi.stop()

