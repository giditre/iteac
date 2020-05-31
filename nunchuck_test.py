from nunchuck import nunchuck
from time import sleep

wii = nunchuck()

#wii.raw()                       # Returns all the data in raw
#wii.joystick()                  # Returns just the X and Y positions of the joystick
#wii.accelerometer()             # Returns X, Y and Z positions of the accelerometer
#wii.button_c()                  # Returns True if C button is pressed, False if not
#wii.button_z()                  # Returns True if Z button is pressed, False if not
#
#wii.joystick_x()                # Returns just the X position of the joystick
#wii.joystick_y()                # Returns just the Y position of the joystick
#wii.accelerometer_x()           # Returns just the X position of the accelerometer
#wii.accelerometer_y()           # Returns just the Y position of the accelerometer
#wii.accelerometer_z()           # Returns just the Z position of the accelerometer
#
#wii.scale(value,min,max,out_min,out_max) # Works the same as Arduino Map, perfect for changing values returned to a different scale, ie -100 - +100

while True:
  
  try:

    print("\rJx {:3d}   Jy {:3d}   Ax {:3d}   Ay {:3d}   Az {:3d}   C {}   Z {}".format(
        wii.scale(wii.joystick_x(), 0, 255, -100, 100),
        wii.scale(wii.joystick_y(), 0, 255, -100, 100),
        wii.scale(wii.accelerometer_x(), 0, 255, -100, 100),
        wii.scale(wii.accelerometer_y(), 0, 255, -100, 100),
        wii.scale(wii.accelerometer_z(), 0, 255, -100, 100),
        1 if wii.button_c() else 0,
        1 if wii.button_z() else 0
    ), end='')

    sleep(0.001)

  except KeyboardInterrupt:
    print()
    break

