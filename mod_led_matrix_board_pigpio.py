import time
import json

import pigpio
import gpio_utils as gu

class LEDMatrixBoard():

  def __init__(self, pi=None, reg_d=11, reg_st=13, reg_sh=15, char_set_file_name="char_sets.json"):

    if pi:
      self.pi = pi
    else:
      self.pi = pigpio.pi()

    self.REG_D = gu.board_to_bcm(reg_d)
    self.REG_ST = gu.board_to_bcm(reg_st)
    self.REG_SH = gu.board_to_bcm(reg_sh)

    self.position_dict = {
      "R3": 0,
      "R6": 1,
      "C5": 2,
      "R8": 3,
      "C3": 4,
      "C2": 5,
      "R7": 6,
      "R5": 7,
      "R1": 8,
      "C4": 9,
      "C6": 10,
      "R4": 11,
      "R2": 12,
      "C1": 13,
      "C7": 14,
      "C8": 15
    }
    
    with open(char_set_file_name) as f:
      self.char_sets = json.load(f)

    self.word_to_wave_id = {}

    #GPIO.setup(self.REG_D, GPIO.OUT)
    #GPIO.setup(self.REG_ST, GPIO.OUT)
    #GPIO.setup(self.REG_SH, GPIO.OUT)

    self.pi.set_mode(self.REG_D, pigpio.OUTPUT)
    self.pi.set_mode(self.REG_ST, pigpio.OUTPUT)
    self.pi.set_mode(self.REG_SH, pigpio.OUTPUT)

    #GPIO.output(self.REG_SH, GPIO.LOW)
    #GPIO.output(self.REG_ST, GPIO.LOW)  

    self.pi.write(self.REG_SH, 0)
    self.pi.write(self.REG_ST, 0)

    self.clear_matrix()

  def store(self):
    #GPIO.output(self.REG_ST, GPIO.HIGH)
    self.pi.write(self.REG_ST, 1)
    #time.sleep(PULSE_DURATION)
    #GPIO.output(self.REG_ST, GPIO.LOW)
    self.pi.write(self.REG_ST, 0)
    #time.sleep(PULSE_DURATION)
  
  def shift(self):
    #GPIO.output(self.REG_SH, GPIO.HIGH)
    self.pi.write(self.REG_SH, 1)
    #time.sleep(PULSE_DURATION)
    #GPIO.output(self.REG_SH, GPIO.LOW)
    self.pi.write(self.REG_SH, 0)
    #time.sleep(PULSE_DURATION)
  
  def out_word(self, word):
    print(word)
    word_key = "{:16s}".format("".join([ str(b) for b in word ]))
    if word_key not in self.word_to_wave_id:
      sq_wave = []
      for i in range(len(word)):
        sq_wave.append(pigpio.pulse(word[i]<<self.REG_D, word[i]<<self.REG_D, 1000))
        sq_wave.append(pigpio.pulse(1<<self.REG_SH, 0<<self.REG_SH, 1000))
        sq_wave.append(pigpio.pulse(0<<self.REG_SH, 1<<self.REG_SH, 1000))
      sq_wave.append(pigpio.pulse(1<<self.REG_ST, 0<<self.REG_ST, 1000))
      sq_wave.append(pigpio.pulse(0<<self.REG_ST, 1<<self.REG_ST, 1000))
      self.pi.wave_add_generic(sq_wave)
      self.word_to_wave_id[word_key] = self.pi.wave_create()
      print(self.word_to_wave_id)
    wid = self.word_to_wave_id[word_key]
    self.pi.wave_send_once(wid)
    while self.pi.wave_tx_busy():
      time.sleep(0.0001)
    #for i in range(len(word)):
    #  #GPIO.output(self.REG_D, word[i])
    #  self.pi.write(self.REG_D, word[i])
    #  self.shift()
    #self.store()
 
  def clear_matrix(self):
    word = 16 * [0]
    self.out_word(word)
  
  def light_dot(self, r, c):
    word = 16 * [0]
    word[self.position_dict["R{}".format(r+1)]] = 1
    for i in range(8):
      word[self.position_dict["C{}".format(i+1)]] = 1
    word[self.position_dict["C{}".format(c+1)]] = 0
    #print(word)
    self.out_word(word)
    #input("Press Enter...")
  
  def light_row(self, row_n, row_values):
    word = 16 * [0]
    word[self.position_dict["R{}".format(row_n+1)]] = 1
    for c in range(8):
      word[self.position_dict["C{}".format(c+1)]] = 0 if row_values[c] else 1
    self.out_word(word)  
  
  def display_image_by_dot(self, image, persistence=0):
    if persistence > 0:
      end_t = time.time() + persistence
    while True:
      for c in range(8):
        for r in range(8):
          if image[r][c]:
            self.light_dot(r,c)
      if persistence > 0 and time.time() >= end_t:
        break
  
  def display_image_by_row(self, image, persistence=0):
    if persistence > 0:
      end_t = time.time() + persistence
    while True:
      for r in range(8):
        #print("row", r, image[r])
        self.light_row(r, image[r])
        #input("Press Enter...")
      if persistence > 0 and time.time() >= end_t:
        break
  
  def display_large_image(self, image, persistence=1):
    # this function is used to display images wider than 8 pixels
    # the height is still assumed to be 8 pixels
    # take image width as lenght of the first row
    image_width = len(image[0])
    #print("image_width", image_width)
    start_c = 0
    while start_c <= image_width-8:
      end_c = start_c + 8
      #print(start_c, end_c)
      frame = [ [ image[r][c] for c in range(start_c, end_c) ] for r in range(8) ]
      #print("frame", frame)
      self.display_image_by_row(frame, persistence)
      start_c += 1
        
  def hex_to_image(self, hex_string):
    #print("hex_string", hex_string)
    binary_string = "{0:064b}".format(int(hex_string, 16))
    #print("binary_string", binary_string)
    rev_binary_string = binary_string[::-1]
    #print("rev binary_string", rev_binary_string)
    image = [ [ int(b) for b in rev_binary_string[i:i+8] ] for i in range(0, 64, 8) ]
    return image
  
  def create_large_image(self, hex_images):
    large_image = [ [] for r in range(8) ]
    for hex_string in hex_images:
      image = self.hex_to_image(hex_string)
      for r in range(8):
        large_image[r] += image[r]
    return large_image
  
  def display_char(self, char, char_set="set1", persistence=0):
    hex_string = self.char_sets[char_set][char]
    image = self.hex_to_image(hex_string)
    self.display_image_by_row(image, persistence)
  
  def display_string_static(self, text, char_set="set1", persistence=1):
    for char in text:
      self.display_char(char, char_set=char_set, persistence=persistence)
  
  def display_string_scroll(self, text, char_set="set1", persistence=1):
    hex_chars = []
    for char in text:
      hex_chars.append(self.char_sets[char_set][char])
    image = self.create_large_image(hex_chars)
    # add left and right blanks
    for r in range(8):
      image[r] = 8*[0] + image[r] + 8*[0]
    self.display_large_image(image, persistence=persistence)

if __name__ == "__main__":

  import datetime

  #import argparse
  #parser = argparse.ArgumentParser()
  
  #parser.add_argument("mand-arg", help="Mandatory positional argument.")
  #parser.add_argument("-c", "--char", help="Character to be displayed", required=False)
  #parser.add_argument("-b", "--opt-arg-b", help="Optional string argument, default: 3", type=int, nargs="?", default=3)
  #parser.add_argument("-c", "--opt-arg-c", help="Optional boolean argument, default: False", action="store_true", default=False)
  
  #args = parser.parse_args()

  pi = pigpio.pi()

  lmb = LEDMatrixBoard(pi)

  try:
    image_G = lmb.hex_to_image("0xffffc3fbfb03ffff")
    image_skull = lmb.hex_to_image("0x2a3e367f49497f3e")
    image_heart = lmb.hex_to_image("0x183c7effffffff66")
    
    while True:

      #lmb.display_string_scroll("{0:%a %d %m %Y %H %M}".format(datetime.datetime.now()), char_set="set2", persistence=0.08)

      lmb.display_image_by_row(image_skull, persistence=1)

      time.sleep(3)

  except KeyboardInterrupt:
    pass
  finally:
    lmb.clear_matrix()
    pi.stop()
