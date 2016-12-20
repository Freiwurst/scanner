#!/usr/bin/env python3
import sys
import division
import Adafruit_PCA9685
from WurstDB.wurstApiClient import DbClient



# Initialise the PCA9685 using the default address (0x40).
pwm = Adafruit_PCA9685.PCA9685()

# Alternatively specify a different address and/or bus:
#pwm = Adafruit_PCA9685.PCA9685(address=0x41, busnum=2)

# Configure min and max servo pulse lengths
servo_min = 150  # Min pulse length out of 4096
servo_max = 600  # Max pulse length out of 4096

# Helper function to make setting a servo pulse width simpler.
def set_servo_pulse(channel, pulse):
    pulse_length = 1000000    # 1,000,000 us per second
    pulse_length //= 60       # 60 Hz
    print('{0}us per period'.format(pulse_length))
    pulse_length //= 4096     # 12 bits of resolution
    print('{0}us per bit'.format(pulse_length))
    pulse *= 1000
    pulse //= pulse_length
    pwm.set_pwm(channel, 0, pulse)

# Set frequency to 60hz, good for servos.
pwm.set_pwm_freq(60)

c = DbClient('None',sys.argv[1])
while True:
    code = input('need wurstcher: ')
    r = c.useCode(code)
    print("%s is %s"%(code,str(r)))
    if r:
        print('Wurst deploment in process')
        pwm.set_pwm(0, 0, servo_max)
        time.sleep(1)
        pwm.set_pwm(0, 0, servo_min)
        time.sleep(1)
        print('Wurst deploment done')

    
