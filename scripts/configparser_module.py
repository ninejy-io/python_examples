import configparser


config = configparser.ConfigParser()
'''
config['DEFAULT'] = {
    'ServerAliveInterval': 60,
    'Compression': 'yes',
    'CompressionLevel': 6,
    'ForwardX11': 'yes'
}

config['bitbucket.org'] = {'User': 'hg'}

config['xxoo.server.com'] = {'Host': 'xxoo.server.com', 'Port': 53321}

with open('example.ini', 'w') as configfile:
    config.write(configfile)
'''

'''
config.read('example.ini')
config.add_section('yuan')
# config.remove_section('bitbucket.org')
# config.remove_option('xxoo.server.com', 'Port')
config.set('bitbucket.org', 'server_id', '1')
config.set('yuan', 'k2', '222222')
config.write(open('new2.ini', 'w'))
'''

config.read('new2.ini')
print(config.sections())
print(config['bitbucket.org']['User'])
print(config.options('yuan'))
print(config.items('bitbucket.org'))
print(config.get('bitbucket.org', 'User'))

