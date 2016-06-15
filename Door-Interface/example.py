# Example code to open a database and query for a card key using doordb

from peewee import SqliteDatabase
import doordb

doordb.init(SqliteDatabase('cards.db'))
user_id = doordb.get_user(card_key = 'hex card key here')
if user_id:
    print "Authenticated user", user_id
else:
    print "Unrecognized card key"
