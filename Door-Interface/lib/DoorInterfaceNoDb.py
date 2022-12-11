import ConfigParser
import binascii
import doordb
import Adafruit_PN532 as PN532

class DoorInterface:


  def __init__(self, path):
    self.config = ConfigParser.ConfigParser()
    self.config.read(path)
    self.card_key = get_hex_array(self.config.get('main', 'key'))
    self.key_block = self.config.getint('main', 'key_block')
    self.id_block = self.config.getint('main', 'id_block')


    self.__key_default = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
    self.__access_key  = get_hex_array( 'FF078069' )

    # Configuration for a Raspberry Pi:
    CS   = 18 # SSEL
    MOSI = 23 # MOSI
    MISO = 24 # MISO
    SCLK = 25 # SCK

    # Create an instance of the PN532 class.
    self.rfid_reader = PN532.PN532(cs=CS, sclk=SCLK, mosi=MOSI, miso=MISO)
    self.rfid_reader.begin()
    self.rfid_reader.SAM_configuration()

  def print_reader_version(self):
    ic, ver, rev, support = self.rfid_reader.get_firmware_version()
    print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))

  def read_card_id(self):
    return self.rfid_reader.read_passive_target()

  def read_block(self, uid, block, key=None):
    "Read the data from the specified block"
    if key is None:
      key = self.card_key
    if self.rfid_reader.mifare_classic_authenticate_block(
                  uid,
                  block,
                  PN532.MIFARE_CMD_AUTH_A,
                  self.card_key):
      return self.rfid_reader.mifare_classic_read_block(block)
    else:
      return None

  def read_key_block(self, uid):
    return self.read_block(uid, self.key_block)

  def read_id_block(self, uid):
    return self.read_block(uid, self.id_block)

  def write_block(self, uid, block, data, key=None):
    if key is None:
      key = self.card_key
    if self.rfid_reader.mifare_classic_authenticate_block(
                  uid,
                  block,
                  PN532.MIFARE_CMD_AUTH_A,
                  key):
      return self.rfid_reader.mifare_classic_write_block(block, data)
    else:
      return None

  def set_key(self, uid):
    "Sets the defined card key on an unused card"
    new_key_data = bytearray( 16 )
    new_key_data[0:6] = self.card_key
    new_key_data[6:10] = self.__access_key
    new_key_data[10:16] = self.__key_default

    return self.write_block(uid, self.key_block, new_key_data, self.__key_default)

  def set_id(self, uid, card_key):
    return self.write_block(uid, self.id_block, get_hex_array(card_key))

  def get_id(self, uid):
    return self.read_id_block(uid)


def get_hex_array ( string ):
  return map( ord, string.decode( "hex" ) )
