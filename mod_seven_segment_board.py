import RPi.GPIO as GPIO
import time
import argparse
import json
import datetime

class SevenSegmentBoard():

  def __init__(self, reg_d=24, reg_st=26, reg_sh=32, addr0=36, addr1=38, addr2=40):
        
    # REG GPIO pins
    self.REG_D = reg_d
    self.REG_ST = reg_st
    self.REG_SH = reg_sh
    # ADDR GPIO pins
    self.ADDR0 = addr0
    self.ADDR1 = addr1
    self.ADDR2 = addr2
    # segment to reg position mapping
    self.segment_dict = {
      "a": 0b00000010,
      "b": 0b00000001,
      "c": 0b00001000,
      "d": 0b00100000,
      "e": 0b00010000,
      "f": 0b10000000,
      "g": 0b01000000,
      "p": 0b00000100
    }
    # char to 7seg mapping
    self.disp_char = {
      "a": "abcefg",
      "b": "cdefg",
      "c": "adef",
      "d": "bcdeg",
      "e": "adefg",
      "f": "aefg",
      "g": "acdef",
      "h": "bcefg",
      "i": "ef",
      "j": "bcde",
      "k": "",
      "l": "def",
      "m": "",
      "n": "ceg",
      "o": "abcdef",
      "p": "abefg",
      "q": "abcfg",
      "r": "eg",
      "s": "acdfg",
      "t": "defg",
      "u": "bcdef",
      "v": "",
      "x": "",
      "y": "bcdfg",
      "z": "abdeg",
      " ": "",
      "0": "abcdef",
      "1": "bc",
      "2": "abdeg",
      "3": "abcdg",
      "4": "bcfg",
      "5": "acdfg",
      "6": "acdefg",
      "7": "abc",
      "8": "abcdefg",
      "9": "abcdfg"
    }
    # char to reg bit mapping
    self.disp_char_segments = {}
    for c in self.disp_char:  
      segments = self.disp_char[c]
      self.disp_char_segments[c] = 0
      for s in segments:
        self.disp_char_segments[c] = self.disp_char_segments[c] | self.segment_dict[s]
    # display position to ADDR mapping
    # ADDR0 ADDR1 ADDR2
    self.addr_list = [
        "110",
        "010",
        "100",
        "000",
        "111",
        "011",
        "101",
        "001"
    ]

    # initialize pins
    GPIO.setmode(GPIO.BOARD)     # use board pin numbers
    GPIO.setup(self.REG_D, GPIO.OUT)  # D
    GPIO.setup(self.REG_ST, GPIO.OUT) # ST
    GPIO.setup(self.REG_SH, GPIO.OUT) # SH

    GPIO.setup(self.ADDR0, GPIO.OUT)
    GPIO.setup(self.ADDR1, GPIO.OUT)
    GPIO.setup(self.ADDR2, GPIO.OUT)

    GPIO.output(self.REG_D, GPIO.LOW)  
    GPIO.output(self.REG_ST, GPIO.LOW)  
    GPIO.output(self.REG_SH, GPIO.LOW)

    GPIO.output(self.ADDR0, GPIO.LOW)
    GPIO.output(self.ADDR1, GPIO.LOW)
    GPIO.output(self.ADDR2, GPIO.LOW)

    self.reg_clear()


  def store(self):
    GPIO.output(self.REG_ST, GPIO.HIGH)
    GPIO.output(self.REG_ST, GPIO.LOW)
  
  def shift(self):
    GPIO.output(self.REG_SH, GPIO.HIGH)
    GPIO.output(self.REG_SH, GPIO.LOW)
  
  def reg_out_sequence(self, seq):
    for i in range(len(seq)):
      GPIO.output(self.REG_D, seq[i]=="1")
      self.shift()
    self.store()
  
  def set_addr(self, a):
    #if a > len(addr_list):
    #  print("a > len(addr_list)")
    #  return
    
    GPIO.output(self.ADDR0, self.addr_list[a][0]=="1")
    GPIO.output(self.ADDR1, self.addr_list[a][1]=="1")
    GPIO.output(self.ADDR2, self.addr_list[a][2]=="1")
  
  def reg_clear(self):
    self.reg_out_sequence("{:08b}".format(0))

 
  def display_text(self, text, active_displays=list(range(8)), persistence=0, char_delay=0.001):
    if len(text) > len(active_displays):
      print("WARNING: you need more than {} displays to display text {} of length {}".format(len(active_displays), text, len(text)))
      text = text[:len(active_displays)]
    if persistence > 0:
      end_t = time.time() + persistence
    else:
      end_t = time.time() + char_delay*len(text)
    #print("end", end_t)
    text = text.lower()
    while time.time() < end_t:
      for i in range(len(text)):
        self.reg_out_sequence("{:08b}".format(self.disp_char_segments[text[i]]))
        self.set_addr(i)
        time.sleep(char_delay)
      #print("time", time.time())
    self.reg_clear()

  def cleanup(self):
    self.reg_clear()
  
if __name__ == '__main__':

  #parser = argparse.ArgumentParser()
  
  #parser.add_argument("mand-arg", help="Mandatory positional argument.")
  #parser.add_argument("-c", "--char", help="Character to be displayed", required=False)
  #parser.add_argument("-b", "--opt-arg-b", help="Optional string argument, default: 3", type=int, nargs="?", default=3)
  #parser.add_argument("-c", "--opt-arg-c", help="Optional boolean argument, default: False", action="store_true", default=False)
  
  #args = parser.parse_args()

  ssb = SevenSegBoard()
  try:
    while True:
      #cb.display_text("lab reti")
      ssb.display_text("{0:%H%M%d%m}".format(datetime.datetime.now()), persistence=5)
  except KeyboardInterrupt:
    pass
  finally:
    ssb.cleanup()
    GPIO.cleanup()
