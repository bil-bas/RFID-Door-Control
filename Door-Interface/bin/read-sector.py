#! /usr/bin/env python

# Read a block from a card with specified block and key.
# Author: Tom Bloor
# lovingly ripped from Adafruits codebase and liberally modified

import ConfigParser
import binascii
import sys

import Adafruit_PN532 as PN532

config = ConfigParser.ConfigParser()
config.read('config.cfg')

def get_hex_array ( string ):
  return map( ord, string.decode( "hex" ) )

key_config = config.get('main', 'key')
key = get_hex_array( key_config )

# Configuration for a Raspberry Pi:
CS   = 18 # SSEL
MOSI = 23 # MOSI
MISO = 24 # MISO
SCLK = 25 # SCK

# Create an instance of the PN532 class.
pn532 = PN532.PN532(cs=CS, sclk=SCLK, mosi=MOSI, miso=MISO)

# Call begin to initialize communication with the PN532.  Must be done before
# any other calls to the PN532!
pn532.begin()

# Get the firmware version from the chip and print it out.
ic, ver, rev, support = pn532.get_firmware_version()
print 'Found PN532 with firmware version: {0}.{1}'.format(ver, rev)

# Configure PN532 to communicate with MiFare cards.
pn532.SAM_configuration()

def read_block(block):
  "Dump the data from the specified block"
  data = pn532.mifare_classic_read_block(block)
  print 'Read block {1}: 0x{0}'.format(binascii.hexlify(data),block)

print 'Waiting for a Card'

flag = True
uid = None

while flag:
  uid = pn532.read_passive_target()

  if uid is not None:
    flag = False

print 'Found card with UID: 0x{0}'.format(binascii.hexlify(uid))

if pn532.mifare_classic_authenticate_block(uid, 4, PN532.MIFARE_CMD_AUTH_A, key):
  read_block(4)
  read_block(5)
  read_block(6)
  read_block(7)
else:
  print 'Failed to Authenticate'

