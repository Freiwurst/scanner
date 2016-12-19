#!/usr/bin/env python3
import sys
from WurstDB.wurstApiClient import DbClient

c = DbClient('None',sys.argv[1])
while True:
    code = input('need wurstcher: ')
    r = c.useCode(code)
    print("%s is %s"%(code,str(r)))
    
