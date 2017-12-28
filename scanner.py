#!/usr/bin/env python3
import logging
from systemd.journal import JournalHandler
import sys
import time
import Adafruit_PCA9685
from WurstDB.wurstApiClient import DbClient

import evdev
from evdev import InputDevice, categorize  # import * is evil :)
dev = InputDevice('/dev/input/by-id/usb-Honeywell_Imaging___Mobility_1900_12054B0617-event-kbd')

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

# Initialise the PCA9685 using the default address (0x40).
pwm = Adafruit_PCA9685.PCA9685()

# Alternatively specify a different address and/or bus:
#pwm = Adafruit_PCA9685.PCA9685(address=0x41, busnum=2)

# Configure min and max servo pulse lengths
servo_min = 235  # Min pulse length out of 4096
servo_max = 450  # Max pulse length out of 4096

# Helper function to make setting a servo pulse width simpler.
def set_servo_pulse(channel, pulse):
    pulse_length = 1000000    # 1,000,000 us per second
    pulse_length //= 50       # 60 Hz
    print('{0}us per period'.format(pulse_length))
    pulse_length //= 4096     # 12 bits of resolution
    print('{0}us per bit'.format(pulse_length))
    pulse *= 1000
    pulse //= pulse_length
    pwm.set_pwm(channel, 0, pulse)

# Set frequency to 60hz, good for servos.
pwm.set_pwm_freq(50)
code = ''
c = DbClient('None',sys.argv[1])
log = logging.getLogger('scanner')
log.addHandler(JournalHandler())
log.setLevel(logging.INFO)
log.info('up and running')
for event in dev.read_loop():
    if event.type == evdev.ecodes.EV_KEY:
        data = evdev.categorize(event)  # Save the event temporarily to introspect it
        if data.keystate == 1:  # Down events only
            if data.scancode == 28:
                print(code)
                if len(code) >= 64:
                    code=code[-64:].lower()
                elif len(code) == 12:
                    code=code[:11].lower()  # kill checksum
                else:
                    log.info("%s is some random code"%(code,str(r)))
                    continue
                r = c.useCode(code)
                log.info("%s is %s"%(code,str(r)))
                if r:
                    print('Wurst deploment in process')
                    pwm.set_pwm(0, 0, servo_max)
                    time.sleep(3)
                    pwm.set_pwm(0, 0, servo_max)
                    time.sleep(7)
                    pwm.set_pwm(0, 0, servo_min)
                    time.sleep(3)
                    pwm.set_pwm(0, 0, servo_min)
                    print('Wurst deploment done')
                else:
                    pwm.set_pwm(1, 0, servo_max)
                    time.sleep(7)
                    pwm.set_pwm(1, 0, servo_min+50)
                code = ''
            else:
                if data.scancode not in scancodes:
                    continue
                code += scancodes.get(data.scancode) 	  				 	 	 	    		  	   		  		



    
