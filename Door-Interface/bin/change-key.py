#! /usr/bin/env python

# Used for changing the key on a Mifare card

import ConfigParser
import binascii
import Adafruit_PN532 as PN532

config = ConfigParser.ConfigParser()
config.read('../config.cfg')

def get_hex_array ( string ):
  return map( ord, string.decode( "hex" ) )

key_config = config.get('main', 'key')
key_new = get_hex_array( key_config )
key_default = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
access_key  = get_hex_array( 'FF078069' )

new_key_data = bytearray( 16 )
new_key_data[0:6] = key_new
new_key_data[6:10] = access_key
new_key_data[10:16] = key_default

CS   = 18 # SSEL
MOSI = 23 # MOSI
MISO = 24 # MISO
SCLK = 25 # SCK

pn532 = PN532.PN532(cs=CS, sclk=SCLK, mosi=MOSI, miso=MISO)
pn532.begin()

ic, ver, rev, support = pn532.get_firmware_version()
print 'Found PN532 with firmware version: {0}.{1}'.format(ver, rev)

# Configure PN532 to communicate with MiFare cards.
pn532.SAM_configuration()

def write_block(block,data):
  "Dump the data to the specified block"
  pn532.mifare_classic_write_block(block,data)
  print 'Wrote to block {1}: 0x{0}'.format(binascii.hexlify(data),block)

print 'Waiting for a Card'

flag = True
uid = None

while flag:
  uid = pn532.read_passive_target()

  if uid is not None:
    flag = False

print 'Found card with UID: 0x{0}'.format(binascii.hexlify(uid))

if pn532.mifare_classic_authenticate_block(uid, 7, PN532.MIFARE_CMD_AUTH_A, key_default):
  print 'Data: {0}'.format(binascii.hexlify(new_key_data))
  write_block(7,new_key_data)
else:
  print 'Failed to Authenticate'

