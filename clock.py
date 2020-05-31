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
  "A": "abcefg",
  "b": "cdef",
  "C": "adef",
  "c": "deg"
}

disp_segments = {}
for c in disp_char:  
  segments = disp_char[c]
  disp_segments[c] = 0
  for s in segments:
    disp_segments[c] = disp_segments[c] | segment_dict[s]

print([bin(disp_segments[s]) for s in disp_segments])

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

def out_word(word):
  for i in range(len(word)):
    GPIO.output(REG_D, word[i]=="1")
    shift()
  store()

def set_addr(a):
  addr_list = [
    (0,0,0),
    (1,0,0),
    (0,1,0),
    (1,1,0),
    (0,0,1),
    (1,0,1),
    (0,1,1),
    (1,1,1)
  ]

  if a > len(addr_list):
    print("a > len(addr_list)")
    return
  
  GPIO.output(ADDR0, addr_list[a][0])
  GPIO.output(ADDR1, addr_list[a][1])
  GPIO.output(ADDR2, addr_list[a][2])

def clear_reg():
  word = 8 * [False]
  out_word(word)

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

  clear_reg()

  #out_word(7*[False]+[True])
  #GPIO.output(REG_D, GPIO.LOW)  

  #out_word(8*[True])

  while True:
    for i in range(0,8,1):
      #print(a)
      #out_word((8-i-1)*[False] + [True] + i*[False])
      out_word("{:08b}".format(disp_segments["A"]))
      #out_word(8*[True])
      set_addr(i)
      time.sleep(0.01)
      shift()
      store()
    #out_word(7*[False]+[True])
    #GPIO.output(REG_D, GPIO.LOW)

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
    clear_reg()
    GPIO.cleanup()
