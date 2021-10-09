import configparser

cfg = configparser.ConfigParser()
cfg.read("config.ini")

host = cfg['mysql']['host']
port = int(cfg['mysql']['port'])
user = cfg['mysql']['user']
password = cfg['mysql']['password']
database = cfg['mysql']['db']

adminPW = cfg['admin portal']['password']