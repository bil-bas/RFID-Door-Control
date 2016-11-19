# Example code to open a database and query for a card key using doordb

import sys
sys.path.append('lib')

from peewee import SqliteDatabase
import doordb

doordb.init(SqliteDatabase('/home/pi/keydb.db'))
#user_id = doordb.get_user(card_key = 'hex card key here')
#if user_id:
#    print "Authenticated user", user_id
#else:
#    print "Unrecognized card key"
for allowed_card in doordb.AllowedCard.select():
  print "ID: %s ; Card: %s " % ( allowed_card.user_id, allowed_card.card_key )
