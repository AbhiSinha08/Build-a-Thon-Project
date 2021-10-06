import configparser

cfg = configparser.ConfigParser()
cfg.read("database.ini")

host = cfg['mysql']['host']
user = cfg['mysql']['user']
password = cfg['mysql']['password']
database = cfg['mysql']['db']

adminPW = cfg['admin']['password']