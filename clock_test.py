import RPi.GPIO as GPIO
import time
import argparse
import json
import datetime

# Define GPIO to REG mapping
REG_D = 24
REG_ST = 26
REG_SH = 32

ADDR0 = 36
ADDR1 = 38
ADDR2 = 40

segment_dict = {
  "a": 0b00000010,
  "b": 0b00000001,
  "c": 0b00001000,
  "d": 0b00100000,
  "e": 0b00010000,
  "f": 0b10000000,
  "g": 0b01000000,
  "p": 0b00000100
}

disp_char = {
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

disp_char_segments = {}
for c in disp_char:  
  segments = disp_char[c]
  disp_char_segments[c] = 0
  for s in segments:
    disp_char_segments[c] = disp_char_segments[c] | segment_dict[s]

#print([bin(disp_char_segments[s]) for s in disp_char_segments])

addr_list = [
    (1,1,0),
    (0,1,0),
    (1,0,0),
    (0,0,0),
    (1,1,1),
    (0,1,1),
    (1,0,1),
    (0,0,1)
]

def store():
  GPIO.output(REG_ST, GPIO.HIGH)
  #time.sleep(PULSE_DURATION)
  GPIO.output(REG_ST, GPIO.LOW)
  #time.sleep(PULSE_DURATION)

def shift():
  GPIO.output(REG_SH, GPIO.HIGH)
  #time.sleep(PULSE_DURATION)
  GPIO.output(REG_SH, GPIO.LOW)
  #time.sleep(PULSE_DURATION)

def reg_out_sequence(seq):
  for i in range(len(seq)):
    GPIO.output(REG_D, seq[i]=="1")
    shift()
  store()

def set_addr(a):
  #if a > len(addr_list):
  #  print("a > len(addr_list)")
  #  return
  
  GPIO.output(ADDR0, addr_list[a][0])
  GPIO.output(ADDR1, addr_list[a][1])
  GPIO.output(ADDR2, addr_list[a][2])

def reg_clear():
  reg_out_sequence("{:08b}".format(0))

def display_text(text, active_displays=list(range(8)), persistence=0, char_delay=0.001):
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
      reg_out_sequence("{:08b}".format(disp_char_segments[text[i]]))
      set_addr(i)
      time.sleep(char_delay)
    #print("time", time.time())

def main(*args, **kwargs):
  
  GPIO.setmode(GPIO.BOARD)     # use board pin numbers
  GPIO.setup(REG_D, GPIO.OUT)  # D
  GPIO.setup(REG_ST, GPIO.OUT) # ST
  GPIO.setup(REG_SH, GPIO.OUT) # SH

  GPIO.setup(ADDR0, GPIO.OUT)
  GPIO.setup(ADDR1, GPIO.OUT)
  GPIO.setup(ADDR2, GPIO.OUT)

  GPIO.output(REG_D, GPIO.LOW)  
  GPIO.output(REG_ST, GPIO.LOW)  
  GPIO.output(REG_SH, GPIO.LOW)

  GPIO.output(ADDR0, GPIO.LOW)
  GPIO.output(ADDR1, GPIO.LOW)
  GPIO.output(ADDR2, GPIO.LOW)

  reg_clear()

  #reg_out_sequence(7*[False]+[True])
  #GPIO.output(REG_D, GPIO.LOW)  

  #reg_out_sequence(8*[True])

  while True:
    #for i in range(3,-1,-1):
    #  #print(a)
    #  #reg_out_sequence((8-i-1)*[False] + [True] + i*[False])
    #  reg_out_sequence("{:08b}".format(disp_char_segments["b"]))
    #  #reg_out_sequence(8*[True])
    #  set_addr(i)
    #  time.sleep(0.125)
    #  shift()
    #  store()
    #reg_out_sequence(7*[False]+[True])
    #GPIO.output(REG_D, GPIO.LOW)
    #display_text("ciaociao")
    #display_text("{0:%H%M%d%m}".format(datetime.datetime.now()), persistence=5)

if __name__ == '__main__':

  #parser = argparse.ArgumentParser()
  
  #parser.add_argument("mand-arg", help="Mandatory positional argument.")
  #parser.add_argument("-c", "--char", help="Character to be displayed", required=False)
  #parser.add_argument("-b", "--opt-arg-b", help="Optional string argument, default: 3", type=int, nargs="?", default=3)
  #parser.add_argument("-c", "--opt-arg-c", help="Optional boolean argument, default: False", action="store_true", default=False)
  
  #args = parser.parse_args()

  try:
    main()
  except KeyboardInterrupt:
    pass
  finally:
    reg_clear()
    GPIO.cleanup()
