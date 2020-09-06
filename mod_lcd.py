#!/usr/bin/python
#--------------------------------------
#    ___  ___  _ ____
#   / _ \/ _ \(_) __/__  __ __
#  / , _/ ___/ /\ \/ _ \/ // /
# /_/|_/_/  /_/___/ .__/\_, /
#                /_/   /___/
#
#  lcd_16x2.py
#  16x2 LCD Test Script
#
# Author : Matt Hawkins
# Date   : 06/04/2015
#
# http://www.raspberrypi-spy.co.uk/
#
# Copyright 2015 Matt Hawkins
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#--------------------------------------

# The wiring for the LCD is as follows:
# 1 : GND
# 2 : 5V
# 3 : Contrast (0-5V)*
# 4 : RS (Register Select)
# 5 : R/W (Read Write)       - GROUND THIS PIN
# 6 : Enable or Strobe
# 7 : Data Bit 0             - NOT USED
# 8 : Data Bit 1             - NOT USED
# 9 : Data Bit 2             - NOT USED
# 10: Data Bit 3             - NOT USED
# 11: Data Bit 4
# 12: Data Bit 5
# 13: Data Bit 6
# 14: Data Bit 7
# 15: LCD Backlight +5V**
# 16: LCD Backlight GND

#import
import RPi.GPIO as GPIO
import time
import argparse

class LCD():

  def __init__(self):

    # Define GPIO to LCD mapping
    self.LCD_POWER = 12
    self.LCD_RS = 19
    self.LCD_E  = 21
    self.LCD_D4 = 23
    self.LCD_D5 = 29
    self.LCD_D6 = 31
    self.LCD_D7 = 33

    # Define some device constants
    self.LCD_WIDTH = 16    # Maximum characters per line
    self.LCD_CHR = True
    self.LCD_CMD = False

    self.LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
    self.LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line

    # Timing constants
    self.E_PULSE = 0.0005
    self.E_DELAY = 0.0005

    #GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)     # use board pin numbers

    GPIO.setup(self.LCD_POWER, GPIO.OUT, initial=GPIO.HIGH)

    GPIO.setup(self.LCD_E, GPIO.OUT)  # E
    GPIO.setup(self.LCD_RS, GPIO.OUT) # RS
    GPIO.setup(self.LCD_D4, GPIO.OUT) # DB4
    GPIO.setup(self.LCD_D5, GPIO.OUT) # DB5
    GPIO.setup(self.LCD_D6, GPIO.OUT) # DB6
    GPIO.setup(self.LCD_D7, GPIO.OUT) # DB7

    self.lcd_init()

  def lcd_on(self):
    # power on (negative logic)
    GPIO.output(self.LCD_POWER, GPIO.LOW)
  
  def lcd_off(self):
    # power off (negative logic)
    GPIO.output(self.LCD_POWER, GPIO.HIGH)
  
  def lcd_init(self):
    self.lcd_on()
    # Initialise display
    self.lcd_byte(0x33, self.LCD_CMD) # 110011 Initialise
    self.lcd_byte(0x32, self.LCD_CMD) # 110010 Initialise
    self.lcd_byte(0x06, self.LCD_CMD) # 000110 Cursor move direction
    self.lcd_byte(0x0C, self.LCD_CMD) # 001100 Display On,Cursor Off, Blink Off
    self.lcd_byte(0x28, self.LCD_CMD) # 101000 Data length, number of lines, font size
    self.lcd_byte(0x01, self.LCD_CMD) # 000001 Clear display
    time.sleep(self.E_DELAY)
  
  def lcd_byte(self, bits, mode):
    # Send byte to data pins
    # bits = data
    # mode = True  for character
    #        False for command
  
    GPIO.output(self.LCD_RS, mode) # RS
  
    # High bits
    GPIO.output(self.LCD_D4, False)
    GPIO.output(self.LCD_D5, False)
    GPIO.output(self.LCD_D6, False)
    GPIO.output(self.LCD_D7, False)
    if bits&0x10==0x10:
      GPIO.output(self.LCD_D4, True)
    if bits&0x20==0x20:
      GPIO.output(self.LCD_D5, True)
    if bits&0x40==0x40:
      GPIO.output(self.LCD_D6, True)
    if bits&0x80==0x80:
      GPIO.output(self.LCD_D7, True)
  
    # Toggle 'Enable' pin
    self.lcd_toggle_enable()
  
    # Low bits
    GPIO.output(self.LCD_D4, False)
    GPIO.output(self.LCD_D5, False)
    GPIO.output(self.LCD_D6, False)
    GPIO.output(self.LCD_D7, False)
    if bits&0x01==0x01:
      GPIO.output(self.LCD_D4, True)
    if bits&0x02==0x02:
      GPIO.output(self.LCD_D5, True)
    if bits&0x04==0x04:
      GPIO.output(self.LCD_D6, True)
    if bits&0x08==0x08:
      GPIO.output(self.LCD_D7, True)
  
    # Toggle 'Enable' pin
    self.lcd_toggle_enable()
  
  def lcd_toggle_enable(self):
    # Toggle enable
    time.sleep(self.E_DELAY)
    GPIO.output(self.LCD_E, True)
    time.sleep(self.E_PULSE)
    GPIO.output(self.LCD_E, False)
    time.sleep(self.E_DELAY)
  
  def lcd_string(self, message, line):
  
    message = message.ljust(self.LCD_WIDTH, " ")
  
    if len(message) > self.LCD_WIDTH:
      print("WARNING: message {} chars, line is {} chars".format(len(message), self.LCD_WIDTH))
  
    self.lcd_byte(line, self.LCD_CMD)
  
    for i in range(self.LCD_WIDTH):
      self.lcd_byte(ord(message[i]), self.LCD_CHR)
  
  def lcd_text(self, message, page_interval=3):
    # divide message in chunks of length LCD_WIDTH
  
    # set first line to write on
    next_line = self.LCD_LINE_1
    # set cursor position in message
    start_position = 0
    while len(message)-start_position > self.LCD_WIDTH:
      # compute end position
      end_position = start_position + self.LCD_WIDTH
      self.lcd_string(message[start_position:end_position], next_line)
      # set next start position in message
      start_position = end_position
      # set next line on LCD
      next_line = self.LCD_LINE_2 if next_line == self.LCD_LINE_1 else self.LCD_LINE_1
      if next_line == self.LCD_LINE_1:
        time.sleep(page_interval)
  
    self.lcd_string(message[start_position:], next_line)

  def clear(self):
    self.lcd_text(2*self.LCD_WIDTH*" ")

  def cleanup(self):
    self.lcd_byte(0x01, self.LCD_CMD)
    #self.lcd_string("Goodbye!",LCD_LINE_1)
    self.lcd_off()


if __name__ == '__main__':

  lcd = LCD()

  try:
    # Initialise display
    #lcd.lcd_init()

    while True:

      text = "It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using 'Content here, content here', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for 'lorem ipsum' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like)."

      # Send some test
      lcd.lcd_text(text, 2)

      # some delay
      # time.sleep(3)

  except KeyboardInterrupt:
    pass
  finally:
    lcd.cleanup()
    GPIO.cleanup()
