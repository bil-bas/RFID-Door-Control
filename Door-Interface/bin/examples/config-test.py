import ConfigParser

config = ConfigParser.ConfigParser()
config.read('config.cfg')

print config.get('main', 'key')
