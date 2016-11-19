# Example code to open a database and query for a card key using doordb

import sys
sys.path.append('lib')

import ConfigParser
import doordb

config = ConfigParser.ConfigParser()
config.read('../config.cfg')

doordb.init(config)
#user_id = doordb.get_user(card_key = 'hex card key here')
#if user_id:
#    print "Authenticated user", user_id
#else:
#    print "Unrecognized card key"
for allowed_card in doordb.AllowedCard.select():
  print "ID: %s ; Card: %s " % ( allowed_card.user_id, allowed_card.card_key )
