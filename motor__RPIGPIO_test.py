import RPi.GPIO as GPIO
import time

IN1_PIN = 31
IN2_PIN = 33
IN3_PIN = 35
IN4_PIN = 37

GPIO.setmode(GPIO.BOARD)

#Read output from PIR motion sensor
GPIO.setup(IN1_PIN, GPIO.OUT)
GPIO.setup(IN2_PIN, GPIO.OUT)
GPIO.setup(IN3_PIN, GPIO.OUT)
GPIO.setup(IN4_PIN, GPIO.OUT)

GPIO.output(IN1_PIN, GPIO.LOW)
GPIO.output(IN2_PIN, GPIO.LOW)
GPIO.output(IN3_PIN, GPIO.LOW)
GPIO.output(IN4_PIN, GPIO.LOW)

while True:
  GPIO.output(IN1_PIN, GPIO.HIGH)
  time.sleep(0.1)
  GPIO.output(IN1_PIN, GPIO.LOW)
  GPIO.output(IN2_PIN, GPIO.HIGH)
  time.sleep(0.1)
  GPIO.output(IN2_PIN, GPIO.LOW)
  GPIO.output(IN3_PIN, GPIO.HIGH)
  time.sleep(0.1)
  GPIO.output(IN3_PIN, GPIO.LOW)
  GPIO.output(IN4_PIN, GPIO.HIGH)
  time.sleep(0.1)
  GPIO.output(IN4_PIN, GPIO.LOW)
  time.sleep(0.1)

