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
#pulse_list = ['0100', '0110', '0010', '1010', '1000', '1001', '0001', '0101']
# counterclockwise
#pulse_list = ['0100', '0101', '0001', '1001', '1000', '1010', '0010', '0110']

pulse_period = 1000

test_wave = []

for pulse in pulse_list:
  neg_pulse = "".join(["0" if b == "1" else "1" for b in pulse])
  print("pulse", pulse, "neg_pulse", neg_pulse)
  test_wave.append( pigpio.pulse( (int(pulse[3])<<A_neg) | (int(pulse[2])<<A_pos) | (int(pulse[1])<<B_neg) | (int(pulse[0])<<B_pos), (int(neg_pulse[3])<<A_neg) | (int(neg_pulse[2])<<A_pos) | (int(neg_pulse[1])<<B_neg) | (int(neg_pulse[0])<<B_pos), pulse_period) )

pi.wave_add_generic(test_wave)
test_wid = pi.wave_create()

try:
  #if clockwise_wid >= 0 and counterclockwise_wid >= 0:
  if test_wid >= 0:
    while True:
      pi.wave_send_once(test_wid)
      while pi.wave_tx_busy():
        time.sleep(0.00001)
      #pi.wave_send_once(clockwise_wid)
      #while pi.wave_tx_busy():
      #  time.sleep(0.00001)
      #pi.wave_send_once(counterclockwise_wid)
      #while pi.wave_tx_busy():
      #  time.sleep(0.00001)
      pi.write(A_neg, 0)
      pi.write(A_pos, 0)
      pi.write(B_neg, 0)
      pi.write(B_pos, 0)
      input("Press Enter")
      #time.sleep(0.1)
  pi.wave_tx_stop()
  pi.wave_delete(test_wid)
  #pi.wave_delete(clockwise_wid)
  #pi.wave_delete(counterclockwise_wid)
except KeyboardInterrupt:
  pi.wave_tx_stop()
  pi.wave_delete(test_wid)
  #pi.wave_delete(clockwise_wid)
  #pi.wave_delete(counterclockwise_wid)
  pass


pi.wave_clear()

pi.write(A_neg, 0)
pi.write(A_pos, 0)
pi.write(B_neg, 0)
pi.write(B_pos, 0)

pi.stop()

