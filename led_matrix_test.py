import RPi.GPIO as GPIO
import time
import argparse
import json

# Define GPIO to REG mapping
REG_D = 11
REG_ST = 13
REG_SH = 15

#PULSE_DURATION = 0.000000001
#
#row_to_index = [15, 10, 9, 12, 1, 7, 2, 5]
#column_to_index = [11, 3, 4, 14, 6, 13, 8, 0]
#reorder_array = row_to_index + column_to_index
#reorder_array_inverted = [ 15-i for i in reorder_array ]
#
#index_to_position = [
#  "R1",
#  "C4",
#  "C6",
#  "R4",
#  "C1",
#  "R2",
#  "R3",
#  "C7",
#  "R6",
#  "C5",
#  "R8",
#  "C3",
#  "C2",
#  "R7",
#  "R5",
#  "C8"
#]

position_dict = {
  "R1": 0,
  "C4": 1,
  "C6": 2,
  "R4": 3,
  "C1": 4,
  "R2": 5,
  "R3": 6,
  "C7": 7,
  "R6": 8,
  "C5": 9,
  "R8": 10,
  "C3": 11,
  "C2": 12,
  "R7": 13,
  "R5": 14,
  "C8": 15
}

with open("char_sets.json") as f:
  char_sets = json.load(f)

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
    GPIO.output(REG_D, word[i])
    shift()
  store()

def clear_matrix():
  word = 16 * [False]
  out_word(word)

def light_dot(r, c):
  word = 16 * [False]
  word[position_dict["R{}".format(r+1)]] = True
  for i in range(8):
    word[position_dict["C{}".format(i+1)]] = True
  word[position_dict["C{}".format(c+1)]] = False
  #print(word)
  out_word(word)
  #input("Press Enter...")

def light_row(row_n, row_values):
  word = 16 * [False]
  word[position_dict["R{}".format(row_n+1)]] = True
  for c in range(8):
    word[position_dict["C{}".format(c+1)]] = not row_values[c]
  out_word(word)  

def display_image_by_dot(image, persistence=0):
  if persistence > 0:
    end_t = time.time() + persistence
  while True:
    for c in range(8):
      for r in range(8):
        if image[r][c]:
          light_dot(r,c)
    if persistence > 0 and time.time() >= end_t:
      break

def display_image_by_row(image, persistence=0):
  if persistence > 0:
    end_t = time.time() + persistence
  while True:
    for r in range(8):
      #print("row", r, image[r])
      light_row(r, image[r])
      #input("Press Enter...")
    if persistence > 0 and time.time() >= end_t:
      break

def display_large_image(image, persistence=1):
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
    display_image_by_row(frame, persistence)
    start_c += 1
      
def hex_to_image(hex_string):
  #print("hex_string", hex_string)
  binary_string = "{0:064b}".format(int(hex_string, 16))
  #print("binary_string", binary_string)
  rev_binary_string = binary_string[::-1]
  #print("rev binary_string", rev_binary_string)
  image = [ [ int(b) for b in rev_binary_string[i:i+8] ] for i in range(0, 64, 8) ]
  return image

def create_large_image(hex_images):
  large_image = [ [] for r in range(8) ]
  for hex_string in hex_images:
    image = hex_to_image(hex_string)
    for r in range(8):
      large_image[r] += image[r]
  return large_image

def display_char(char, char_set="set1", persistence=0):
  hex_string = char_sets["{}_{}".format(char_set, char)]
  image = hex_to_image(hex_string)
  display_image_by_row(image, persistence)

def display_string_static(text, char_set="set1", persistence=1):
  for char in text:
    display_char(char, char_set=char_set, persistence=persistence)

def display_string_scroll(text, char_set="set1", persistence=1):
  hex_chars = []
  for char in text:
    hex_chars.append(char_sets["{}_{}".format(char_set, char)])
  image = create_large_image(hex_chars)
  # add left and right blanks
  for r in range(8):
    image[r] = 8*[0] + image[r] + 8*[0]
  display_large_image(image, persistence=persistence)

def main():
  
  #GPIO.setwarnings(False)
  GPIO.setmode(GPIO.BOARD)     # use board pin numbers
  GPIO.setup(REG_D, GPIO.OUT)  # D
  GPIO.setup(REG_ST, GPIO.OUT) # ST
  GPIO.setup(REG_SH, GPIO.OUT) # SH

  GPIO.output(REG_SH, GPIO.LOW)
  GPIO.output(REG_ST, GPIO.LOW)  

  clear_matrix()

  #word[position_dict["R1"]] = True
  #word[position_dict["R8"]] = True
  #for i in range(1, 8+1):
  #  word[position_dict["C{}".format(i)]] = True
  #word[position_dict["C1"]] = False
  #word[position_dict["C8"]] = False
  #print(word)
  #out_word(word)
  #input("Press Enter...")


  #light_dot(5, 8)
  #for i in range(8):
  #  light_row(i, image[i])
  #  input("Press Enter...")
  #display_image_by_row(image)

  image_G = hex_to_image("0xffffc3fbfb03ffff")
  image_skull = hex_to_image("0x2a3e367f49497f3e")
  image_heart = hex_to_image("0x183c7effffffff66")
  
  #display_image_by_row(image_heart)
  
  #display_char("K")

  #display_string_static("Ciao")

  #large_image = create_large_image(["0x183c7effffffff66", "0x2a3e367f49497f3e"])
  #print(large_image)
  #display_large_image(large_image, persistence=0.5)
  

  #clear_matrix()

  while True:

    display_string_scroll("This is a very long text", persistence=1.1)
    #display_image_by_row(image_skull, persistence=1)

    time.sleep(3)

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
    clear_matrix()
    GPIO.cleanup()
