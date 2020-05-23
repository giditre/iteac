import time
import sys
import json
import math
import pigpio

# Write (Floppy Pin 22)
# BOARD 29 - BCM 5
WRITE = 5
# Step (Floppy Pin 20)
# BOARD 31 - BCM 6
STEP = 6
# Direction (Floppy Pin 18)
# BOARD 33 - BCM 13
DIR = 13

###

DIR_FWD = 0
DIR_BCK = 1

N_ST_RESET = 80

###

POSITION = 0
DIRECTION = DIR_FWD

###

pi = pigpio.pi() # connect to local Pi

pi.set_mode(STEP, pigpio.OUTPUT)
pi.set_mode(DIR, pigpio.OUTPUT)
pi.set_mode(WRITE, pigpio.OUTPUT)

pi.wave_clear()

# reset position
# move the head the maximum amount of steps back
pi.write(DIR, DIR_BCK)
for s in range(N_ST_RESET+1):
  # send one step pulse
  pi.write(STEP, 1)
  time.sleep(0.001)
  pi.write(STEP, 0)
  time.sleep(0.001)

#def create_sq_wave(freq, pin):
#  # compute period based on frequency
#  period = 1.0/freq
#  # convert period in us
#  period = int(period*1e6)
#  semiperiod = int(period/2)
#  print(freq, period, semiperiod)
#  sq_wave = []
#  # PIN ON MASK, PIN OFF MASK, MICROS
#  sq_wave.append(pigpio.pulse(1<<pin, 0, semiperiod))
#  sq_wave.append(pigpio.pulse(0, 0<<pin, semiperiod))
#
#  pi.wave_add_generic(sq_wave)
#
#  wave_id = pi.wave_create()
#
#  return wave_id

#with open("tonelist_mariovictory.json") as f:
with open("tonelist_imperialmarch.json") as f:
  tone_json = json.load(f)

tone_list = tone_json["sequence"]

limit = min(42, len(tone_list))

#freq_list = [100, 200, 300, 600]
freq_list = [ tone["f"] for tone in tone_list[:limit] ]
duration_list = [ float(tone["l"]/1000.0) for tone in tone_list[:limit] ]
pause_list = [ float(tone["d"]/1000.0) if "d" in tone else 0 for tone in tone_list[:limit] ]

print(freq_list)

max_freq = max(freq_list)
if max_freq > 440:
  shift_factor = max_freq/440.0
  freq_list = [ int(f/shift_factor) for f in freq_list ]

print(freq_list)

#sys.exit()

sq_wave = []

for freq, duration, pause in zip(freq_list, duration_list, pause_list):

  period = int((1.0/freq)*1e6)
  semiperiod = int(period/2)

  remaining_steps = int(freq * duration)

  #print(freq, duration, period, semiperiod, remaining_steps)

  while remaining_steps > 0:
    #print("in while loop", remaining_steps, POSITION, "FWD" if DIRECTION == DIR_FWD else "BCK")
    tmp = []
    if DIRECTION == DIR_FWD:
      tmp.append(pigpio.pulse((1<<STEP)|(0<<DIR), (0<<STEP)|(1<<DIR), semiperiod))
      tmp.append(pigpio.pulse((0<<STEP)|(0<<DIR), (1<<STEP)|(1<<DIR), semiperiod))
    else:
      tmp.append(pigpio.pulse((1<<STEP)|(1<<DIR), (0<<STEP)|(0<<DIR), semiperiod))
      tmp.append(pigpio.pulse((0<<STEP)|(1<<DIR), (1<<STEP)|(0<<DIR), semiperiod))
      
    # compute number of steps to take in current direction, based on current position
    tmp_steps = min(remaining_steps, 80-POSITION if DIRECTION == DIR_FWD else POSITION)

    # add steps (pulses) to waveform
    sq_wave.extend(tmp_steps*tmp)

    # update number of residual steps
    remaining_steps -= tmp_steps

    # update current position
    POSITION = POSITION+tmp_steps if DIRECTION == DIR_FWD else POSITION-tmp_steps
    # if drive head has reached one of the boundaries (POSITION 0 or 80), invert direction
    if POSITION == 0:
      DIRECTION = DIR_FWD
    elif POSITION == 80:
      DIRECTION = DIR_BCK

  # pause
  # convert pause in us
  pause = int(pause*1e6)
  tmp = []
  tmp.append(pigpio.pulse(0, 0, pause))
  sq_wave.extend(tmp)

pi.wave_add_generic(sq_wave)
wid = pi.wave_create()
#print(wid)

try:
  if wid >= 0:
    t1 = time.time()
    pi.wave_send_once(wid)
    while pi.wave_tx_busy():
      time.sleep(0.01)
    t2 = time.time()
    print(t2-t1)
    pi.wave_tx_stop()
    pi.wave_delete(wid)
except KeyboardInterrupt:
  pi.wave_tx_stop()
  pi.wave_delete(wid)
  pi.stop()

pi.wave_clear()
pi.stop()
