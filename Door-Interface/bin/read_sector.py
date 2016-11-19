# Script will loop and print any card id's it finds

# Hack to allow you to run with virtualenv under sudo
# https://virtualenv.pypa.io/en/latest/userguide/#using-virtualenv-without-bin-python
activate_this = 'env/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

import sys
sys.path.append('lib')

import signal
import binascii
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
  uid = None
  uid = interface.read_card_id()

  if uid is not None:
    print 'Found card with UID: 0x{0}'.format(binascii.hexlify(uid))
    data = interface.read_block(uid)
    if data is not None:
      print 'Read block {1}: 0x{0}'.format(binascii.hexlify(data),interface.card_block)
    else:
      print "Failed to read block"
    time.sleep(2)

