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

try:
  user_id = sys.argv[1]
except:
  print "You must supply a user id!"
  sys.exit(1)

print 'Setting up...'

interface = DoorInterface('../config.cfg')
interface.print_reader_version()

def signal_handler(signal, frame):
  print "\nStopping Scanning"
  sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

print 'Present Card to change Key on...'

uid = None
while uid is None:
  uid = interface.read_card_id()

  if uid is not None:
    print 'Found card with UID: 0x{0}'.format(binascii.hexlify(uid))
    if interface.set_id(uid, user_id):
      print 'Changed key in card'
    else:
      print "Failed to change key"

