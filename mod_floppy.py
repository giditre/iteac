import time
import sys
import json
import math
import pigpio

import gpio_utils as gu

class FloppyDrive():

  def __init__(self, pi=None, write=29, step=31, direction=33):

    # Write (Floppy Pin 22)
    self.WRITE = gu.board_to_bcm(write)
    # Step (Floppy Pin 20)
    self.STEP = gu.board_to_bcm(step)
    # Direction (Floppy Pin 18)
    self.DIR = gu.board_to_bcm(direction)
    
    # direction to logic level mapping
    self.DIR_FWD = 0
    self.DIR_BCK = 1
    
    # number of steps sback to take to position reset
    self.N_ST_RESET = 80
    
    # initialize head position (0 to 80)
    self.POSITION = 0
    self.DIRECTION = self.DIR_FWD
    
    if pi:
      self.pi = pi
    else:
      self.pi = pigpio.pi() # connect to local Pi

    self.pi.set_mode(self.STEP, pigpio.OUTPUT)
    self.pi.set_mode(self.DIR, pigpio.OUTPUT)
    self.pi.set_mode(self.WRITE, pigpio.OUTPUT)

    self.pi.wave_clear()

    # reset position
    self.pi.write(self.DIR, self.DIR_BCK)
    for s in range(self.N_ST_RESET+1):
      # send one step pulse
      self.pi.write(self.STEP, 1)
      time.sleep(0.001)
      self.pi.write(self.STEP, 0)
      time.sleep(0.001)

  def generate_wave(self, json_file_name, n_tones_limit=42, freq_limit=440):

    with open(json_file_name) as f:
      tone_json = json.load(f)
    
    tone_list = tone_json["sequence"]
    
    limit = min(n_tones_limit, len(tone_list))
    
    freq_list = [ tone["f"] for tone in tone_list[:limit] ]
    duration_list = [ float(tone["l"]/1000.0) for tone in tone_list[:limit] ]
    pause_list = [ float(tone["d"]/1000.0) if "d" in tone else 0 for tone in tone_list[:limit] ]
    
    #print(freq_list)
    
    max_freq = max(freq_list)
    freq_limit = float(freq_limit)
    if max_freq > freq_limit:
      shift_factor = max_freq/freq_limit
      freq_list = [ int(f/shift_factor) for f in freq_list ]
    
    #print(freq_list)
    
    sq_wave = []
    
    for freq, duration, pause in zip(freq_list, duration_list, pause_list):
    
      period = int((1.0/freq)*1e6)
      semiperiod = int(period/2)
    
      remaining_steps = int(freq * duration)
    
      #print(freq, duration, period, semiperiod, remaining_steps)
    
      while remaining_steps > 0:
        #print("in while loop", remaining_steps, POSITION, "FWD" if DIRECTION == DIR_FWD else "BCK")
        tmp = []
        if self.DIRECTION == self.DIR_FWD:
          tmp.append(pigpio.pulse((1<<self.STEP)|(0<<self.DIR),
            (0<<self.STEP)|(1<<self.DIR), semiperiod))
          tmp.append(pigpio.pulse((0<<self.STEP)|(0<<self.DIR),
            (1<<self.STEP)|(1<<self.DIR), semiperiod))
        else:
          tmp.append(pigpio.pulse((1<<self.STEP)|(1<<self.DIR),
            (0<<self.STEP)|(0<<self.DIR), semiperiod))
          tmp.append(pigpio.pulse((0<<self.STEP)|(1<<self.DIR),
            (1<<self.STEP)|(0<<self.DIR), semiperiod))
          
        # compute number of steps to take in current direction, based on current position
        tmp_steps = min(remaining_steps, 80-self.POSITION if self.DIRECTION == self.DIR_FWD else self.POSITION)
    
        # add steps (pulses) to waveform
        sq_wave.extend(tmp_steps*tmp)
    
        # update number of residual steps
        remaining_steps -= tmp_steps
    
        # update current position
        self.POSITION = self.POSITION+tmp_steps if self.DIRECTION == self.DIR_FWD else self.POSITION-tmp_steps
        # if drive head has reached one of the boundaries (POSITION 0 or 80), invert direction
        if self.POSITION == 0:
          self.DIRECTION = self.DIR_FWD
        elif self.POSITION == 80:
          self.DIRECTION = self.DIR_BCK
    
      # pause
      # convert pause in us
      pause = int(pause*1e6)
      tmp = []
      tmp.append(pigpio.pulse(0, 0, pause))
      sq_wave.extend(tmp)

    return sq_wave[:]

if __name__ == "__main__":

  pi = pigpio.pi()

  fdr = FloppyDrive(pi) 
 
  sq_wave = fdr.generate_wave("tonelist_imperialmarch.json")

  pi.wave_add_generic(sq_wave)

  wid = pi.wave_create()
  print(wid)

  try:
    if wid >= 0:
      t1 = time.time()
      pi.wave_send_once(wid)
      while pi.wave_tx_busy():
        time.sleep(0.01)
      t2 = time.time()
      print(t2-t1)
  except KeyboardInterrupt:
    pass
  finally:
    pi.wave_tx_stop()
    pi.wave_delete(wid)
    pi.wave_clear()
    pi.stop()
