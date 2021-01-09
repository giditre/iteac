import ctypes
import pathlib

from datetime import datetime

import time

position_dict = {
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

def row_values_to_word(row_values, row_n):
  print("row_values", row_values, row_n)
  word = 16 * [0]
  word[position_dict["R{}".format(row_n+1)]] = 1
  #print(word)
  for c in range(8):
    if row_values[c] == "1":
      word[position_dict["C{}".format(c+1)]] = 0
    else:
      word[position_dict["C{}".format(c+1)]] = 1
  #print(word)
  word = "".join([str(c) for c in word])
  print(word)
  return word
  #return int(word, 2) # base 2

def bits_to_frame(binary_string):
  assert len(binary_string) == 64, ""
  binary_string = binary_string[::-1]
  #print(binary_string)
  frame = [ row_values_to_word(binary_string[i:i+8], int(i/8)) for i in range(0, 64, 8) ]
  #print("frame", [ "{:b}".format(r) for r in frame ])
  print("frame", [ r for r in frame ])
  return frame


def hex_to_frame(hex_string):
  binary_string = "{0:064b}".format(int(hex_string, 16))
  #print(binary_string)
  return bits_to_frame(binary_string)

def create_large_image(hex_string_list):
  large_image = [ [] for r in range(8) ]
  for hex_string in hex_string_list:
    # create single panel
    binary_string = "{0:064b}".format(int(hex_string, 16))
    rev_binary_string = binary_string[::-1]
    image = [ [ int(b) for b in rev_binary_string[i:i+8] ] for i in range(0, 64, 8) ]
    # concatenate panels
    for r in range(8):
      large_image[r] += image[r]
  print("large_image", large_image)
  return large_image

#def display_large_image(image, persistence=1):
#  # this function is used to display images wider than 8 pixels
#  # the height is still assumed to be 8 pixels
#  # take image width as lenght of the first row
#  image_width = len(image[0])
#  #print("image_width", image_width)
#  start_c = 0
#  while start_c <= image_width-8:
#    end_c = start_c + 8
#    #print(start_c, end_c)
#    frame = [ [ image[r][c] for c in range(start_c, end_c) ] for r in range(8) ]
#    #print("frame", frame)
#    self.display_image_by_row(frame, persistence)
#    start_c += 1

libname = pathlib.Path().absolute() / "libmatrix.so"
c_lib = ctypes.CDLL(libname)
#c_lib.display_digits.restype = ctypes.c_int

duration = 1

c_lib.gpio_setup()

#c_lib.display_digits((ctypes.c_int * len(digits))(*digits), ctypes.c_int(len(digits)), ctypes.c_int(duration))
#c_lib.light_word(ctypes.c_uint16(int("0xff00", 16)))
#time.sleep(duration)
#rows = [int("0x1000", 16)] * 8

hex_string_G = "0xffffc3fbfb03ffff" # capital G
hex_string_skull = "0x2a3e367f49497f3e" # skull
hex_string_heart = "0x183c7effffffff66" # heart

frame = [ int(row, 2) for row in hex_to_frame(hex_string_heart) ]
c_lib.light_matrix((ctypes.c_uint16 * len(frame))(*frame), duration)

image = create_large_image([hex_string_heart, hex_string_skull])
image_width = len(image[0])
#print("image_width", image_width)
start_c = 0
while start_c <= image_width-8:
  end_c = start_c + 8
  print(start_c, end_c)
  binary_string = ""
  for r in range(7, -1, -1):
    binary_string += "".join([str(b) for b in image[r][start_c:end_c]])
  print(binary_string)
  frame = [ int(row, 2) for row in bits_to_frame(binary_string) ]
  c_lib.light_matrix((ctypes.c_uint16 * len(frame))(*frame), duration) 
  start_c += 1


c_lib.clear()
