# Script will loop and print any card id's it finds

# Hack to allow you to run with virtualenv under sudo
# https://virtualenv.pypa.io/en/latest/userguide/#using-virtualenv-without-bin-python
activate_this = 'env/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

import sys
sys.path.append('lib')

import signal
import time
from DoorInterface import DoorInterface

print 'Setting up...'

interface = DoorInterface('../config.cfg')
interface.print_reader_version()

def signal_handler(signal, frame):
  print "\nStopping Scanning"
  sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

while 1:
  flag = interface.check_card()

  if flag is True:
    print "Opening Door"
    time.sleep(5)

  time.sleep(1)
