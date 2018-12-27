#!/usr/bin/env python3
import pigpio
import logging
from systemd.journal import JournalHandler
import sys
import time
import Adafruit_PCA9685
from WurstDB.wurstApiClient import DbClient
import threading

import evdev
from evdev import InputDevice, categorize  # import * is evil :)
dev = InputDevice('/dev/input/by-id/usb-NEWTOLOGIC_NEWTOLOGIC-event-kbd')

pi = pigpio.pi()
shooterPin = 4
signPin = 18
doNotDie = True
def scanner():
    scannerMin = 510
    scannerPin = 27
    scannerMax = 1000
    scannerState = True
    lastTime = time.time()
    pi2 = pigpio.pi()
    while(True):
        if (time.time() - lastTime > 1):
            log.info('now')
            if scannerState:
                scannerState = False
                pi2.set_servo_pulsewidth(scannerPin, scannerMax)
            else:
                scannerState = True 
                pi2.set_servo_pulsewidth(scannerPin, scannerMin)
            lastTime = time.time()
            log.info('servo done')
# Provided as an example taken from my own keyboard attached to a Centos 6 box:
scancodes = {
    # Scancode: ASCIICode
    0: None, 2: u'1', 3: u'2', 4: u'3', 5: u'4', 6: u'5', 7: u'6', 8: u'7', 9: u'8',
    10: u'9', 11: u'0', 12: u'-', 13: u'=', 16: u'Q', 17: u'W', 18: u'E', 19: u'R',
    20: u'T', 21: u'Z', 22: u'U', 23: u'I', 24: u'O', 25: u'P', 26: u'[', 27: u']',
    30: u'A', 31: u'S', 32: u'D', 33: u'F', 34: u'G', 35: u'H', 36: u'J', 37: u'K', 38: u'L', 39: u';',
    40: u'"', 41: u'`', 42: u'', 43: u'\\', 44: u'Y', 45: u'X', 46: u'C', 47: u'V', 48: u'B', 49: u'N',
    50: u'M', 51: u',', 52: u'.', 53: u'/'
}

dev.grab()

# Configure min and max servo pulse lengths
servo_min = 1100  # Min pulse length out of 4096
servo_max = 1980  # Max pulse length out of 4096


# Set frequency to 60hz, good for servos.
code = ''
c = DbClient('None',sys.argv[1])
log = logging.getLogger('scanner')
log.addHandler(JournalHandler())
log.setLevel(logging.INFO)
log.info('up and running')
pi.set_PWM_frequency(shooterPin, 50)
pi.set_PWM_frequency(signPin, 50)
pi.set_PWM_range(signPin, 1000)

time.sleep(3)

for event in dev.read_loop():
    if event.type == evdev.ecodes.EV_KEY:
        data = evdev.categorize(event)  # Save the event temporarily to introspect it
        if data.keystate == 1:  # Down events only
            if data.scancode == 28:

                log.info('scancode 28  #%s# '%(code,))
                print(code)
                if len(code) >= 64:
                    code=code[-64:].lower()
                elif len(code) == 12:
                    code=code[:11].lower()  # kill checksum
                else:
                    continue
                r = c.useCode(code)
                log.info("%s is %s"%(code,str(r)))
                if r:
                    print('Wurst deploment in process')
                    pi.set_servo_pulsewidth(shooterPin, servo_max)
                    time.sleep(3)
                    pi.set_servo_pulsewidth(shooterPin, servo_max)
                    time.sleep(7)
                    pi.set_servo_pulsewidth(shooterPin, servo_min)
                    time.sleep(3)
                    pi.set_servo_pulsewidth(shooterPin, servo_min)
                    print('Wurst deploment done')
                else:
                    pi.set_servo_pulsewidth(signPin, servo_max)
                    time.sleep(7)
                    pi.set_servo_pulsewidth(signPin, servo_min)
                code = ''
            else:
                if data.scancode not in scancodes:
                    continue
                code += scancodes.get(data.scancode) 	  				 	 	 	    		  	   		  		



    
