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

pulse_period = 1000

clockwise_wave = []

clockwise_wave.append(pigpio.pulse((1<<A_neg)|(0<<A_pos)|(1<<B_neg)|(0<<B_pos), (0<<A_neg)|(1<<A_pos)|(0<<B_neg)|(1<<B_pos), pulse_period))
clockwise_wave.append(pigpio.pulse((1<<A_neg)|(1<<A_pos)|(0<<B_neg)|(1<<B_pos), (0<<A_neg)|(0<<A_pos)|(1<<B_neg)|(0<<B_pos), pulse_period))
clockwise_wave.append(pigpio.pulse((1<<A_neg)|(1<<A_pos)|(0<<B_neg)|(0<<B_pos), (0<<A_neg)|(0<<A_pos)|(1<<B_neg)|(1<<B_pos), pulse_period))
clockwise_wave.append(pigpio.pulse((0<<A_neg)|(1<<A_pos)|(0<<B_neg)|(0<<B_pos), (1<<A_neg)|(0<<A_pos)|(1<<B_neg)|(1<<B_pos), pulse_period))
clockwise_wave.append(pigpio.pulse((0<<A_neg)|(0<<A_pos)|(0<<B_neg)|(0<<B_pos), (1<<A_neg)|(1<<A_pos)|(1<<B_neg)|(1<<B_pos), pulse_period))

pi.wave_add_generic(clockwise_wave)
clockwise_wid = pi.wave_create()

counterclockwise_wave = []

counterclockwise_wave.append(pigpio.pulse((0<<A_neg)|(1<<A_pos)|(0<<B_neg)|(1<<B_pos), (1<<A_neg)|(0<<A_pos)|(1<<B_neg)|(0<<B_pos), pulse_period))
counterclockwise_wave.append(pigpio.pulse((1<<A_neg)|(0<<A_pos)|(1<<B_neg)|(1<<B_pos), (0<<A_neg)|(1<<A_pos)|(0<<B_neg)|(0<<B_pos), pulse_period))
counterclockwise_wave.append(pigpio.pulse((1<<A_neg)|(1<<A_pos)|(0<<B_neg)|(0<<B_pos), (0<<A_neg)|(0<<A_pos)|(1<<B_neg)|(1<<B_pos), pulse_period))
counterclockwise_wave.append(pigpio.pulse((0<<A_neg)|(0<<A_pos)|(1<<B_neg)|(0<<B_pos), (1<<A_neg)|(1<<A_pos)|(0<<B_neg)|(1<<B_pos), pulse_period))
counterclockwise_wave.append(pigpio.pulse((0<<A_neg)|(0<<A_pos)|(0<<B_neg)|(0<<B_pos), (1<<A_neg)|(1<<A_pos)|(1<<B_neg)|(1<<B_pos), pulse_period))

pi.wave_add_generic(counterclockwise_wave)
counterclockwise_wid = pi.wave_create()

try:
  if clockwise_wid >= 0 and counterclockwise_wid >= 0:
    while True:
      pi.wave_send_once(clockwise_wid)
      while pi.wave_tx_busy():
        time.sleep(0.00001)
      pi.wave_send_once(counterclockwise_wid)
      while pi.wave_tx_busy():
        time.sleep(0.00001)
      #pi.write(A_neg, 0)
      #pi.write(A_pos, 0)
      #pi.write(B_neg, 0)
      #pi.write(B_pos, 0)
      input("Press Enter")
  pi.wave_tx_stop()
  pi.wave_delete(clockwise_wid)
  pi.wave_delete(counterclockwise_wid)
except KeyboardInterrupt:
  pi.wave_tx_stop()
  pi.wave_delete(clockwise_wid)
  pi.wave_delete(counterclockwise_wid)
  pass


pi.wave_clear()

pi.write(A_neg, 0)
pi.write(A_pos, 0)
pi.write(B_neg, 0)
pi.write(B_pos, 0)

pi.stop()

