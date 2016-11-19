import ConfigParser
import doordb
import Adafruit_PN532 as PN532

class DoorInterface:

  db = doordb

  def __init__(self, path):
    self.config = ConfigParser.ConfigParser()
    self.config.read(path)
    self.db.init(self.config)
    self.card_key = get_hex_array(self.config.get('main', 'key'))

    # Configuration for a Raspberry Pi:
    CS   = 18 # SSEL
    MOSI = 23 # MOSI
    MISO = 24 # MISO
    SCLK = 25 # SCK

    # Create an instance of the PN532 class.
    self.rfid_reader = PN532.PN532(cs=CS, sclk=SCLK, mosi=MOSI, miso=MISO)
    self.rfid_reader.begin()

  def dump_cards(self):
    for allowed_card in self.db.AllowedCard.select():
      print "ID: %s ; Card: %s " % ( allowed_card.user_id, allowed_card.card_key )

  def print_reader_version(self):
    ic, ver, rev, support = self.rfid_reader.get_firmware_version()
    print 'Found PN532 with firmware version: {0}.{1}'.format(ver, rev)

  def read_card_id(self):
    return self.rfid_reader.read_passive_target()

def get_hex_array ( string ):
  return map( ord, string.decode( "hex" ) )
