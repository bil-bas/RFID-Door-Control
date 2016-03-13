from peewee import *

# Use a proxy because we don't know what the database is until runtime
db_proxy = Proxy()

# Use a base model class to make sure all subclasses automatically use the right database
class BaseModel(Model):
    class Meta:
        database = db_proxy

class AllowedCard(BaseModel):
    user_id = IntegerField(primary_key=True)
    card_key = CharField(max_length=64)

    class Meta:
        db_table='allowed_cards'

"""
Initialize doordb with a peewee database.  E.g., init(peewee.SqliteDatabase('cards.db'))
:param db: a peewee database descriptor
"""
def init(db):
    db_proxy.initialize(db)
    db_proxy.connect()

"""
Close the database connection
"""
def close():
    db_proxy.close()

"""
Get a user ID from a card key

:param card_key: The card key, in hex
:return: returns the ID of the user who holds that card, or None if the card key is not recognized
"""
def get_user(card_key):
    card = AllowedCard.select().where(AllowedCard.card_key == card_key).first()
    if card:
        return card.user_id
    else:
        return None
