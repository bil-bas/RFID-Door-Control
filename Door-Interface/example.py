# Example code to open a database and query for a card key using doordb

# Hack to allow you to run with virtualenv under sudo
# https://virtualenv.pypa.io/en/latest/userguide/#using-virtualenv-without-bin-python
activate_this = 'env/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

import sys
sys.path.append('lib')

from DoorInterface import DoorInterface

interface = DoorInterface('../config.cfg')
interface.dump_cards()
interface.print_reader_version()

#doordb.init(config)
#user_id = doordb.get_user(card_key = 'hex card key here')
#if user_id:
#    print "Authenticated user", user_id
#else:
#    print "Unrecognized card key"
