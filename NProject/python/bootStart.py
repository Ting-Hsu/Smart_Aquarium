#!/usr/bin/python3
import sys
import time
import smbus2
from picamera import PiCamera
from gpiozero import Button
from time import sleep
from gpiozero import LED
import os
import glob
from RPLCD.i2c import CharLCD

camera = PiCamera()
led = LED(5)
button = Button(17)
sys.modules['smbus'] = smbus2
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave' 
lcd = CharLCD('PCF8574', address=0x27, port=1, backlight_enabled=True)
  
def read_device_file():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def parse_temperature():
    lines = read_device_file()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.1)
        lines = read_device_file()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temperature_string = lines[1][equals_pos+2:]
        temperature_c = float(temperature_string) / 1000.0
        return temperature_c
 
try:
    print('按下 Ctrl-C 可停止程式')
    lcd.clear()
    while True:
        if button.is_pressed:
            #print("Pressed")
            led.on()
            lcd.cursor_pos = (0, 0)
            lcd.write_string("bt click")
            localtime = time.localtime(time.time())
            if localtime.tm_sec % 5 == 0:
               
                c= parse_temperature()
                print('溫度為攝氏 {:.2f} 度'.format(c))
                lcd.cursor_pos = (0, 11)
                lcd.write_string(str(round(c,1))+"C")
                camera.capture('/home/pi/Desktop/Images/test.jpg')
                #print(timestr)
                #timestr = time.strftime("%Y%m%d-%H%M%S")
                #camera.capture('/home/pi/Desktop/Images/'+timestr+'.jpg')
        else:
            #print("Released")
            led.off()
            lcd.cursor_pos = (0, 0)
            lcd.write_string("bt moved")
                    
        lcd.cursor_pos = (1, 0)
        lcd.write_string("Time: {}".format(time.strftime("%H:%M:%S")))
        time.sleep(0.2)
except KeyboardInterrupt:
    print('關閉程式')
finally:
    lcd.clear()
