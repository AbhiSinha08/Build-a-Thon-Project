""" File: cfg.py / config.py """
""" To collect and parse data from config files (config.ini and notifications.ini) """

import configparser

cfg = configparser.ConfigParser()

# Parsing configuration from config.ini
cfg.read("config.ini")

# MySQL Configuration
HOST = cfg['mysql']['host']
PORT = int(cfg['mysql']['port'])
USER = cfg['mysql']['user']
PASSWORD = cfg['mysql']['password']
DATABASE = cfg['mysql']['db']

# Password for admin portal
ADMIN_PW = cfg['admin portal']['password']

# Credentials for email id to send mails
MAIL_ID = cfg['mail bot']['mail_id']
MAIL_PASSWORD = cfg['mail bot']['password']
SMTP_SERVER = cfg['mail bot']['smtp_server']
SMTP_PORT = int(cfg['mail bot']['port'])
SUBJECT = cfg['mail bot']['subject']

# Option to enable whatsapp messages to users
WA_OPTION = cfg['whatsapp']['enable'].upper()
if WA_OPTION == "YES" or WA_OPTION == "Y":
    WA_OPTION = True
else:
    WA_OPTION = False

API = cfg['sms bot']['API']


# Parsing configuration from notifications.ini
cfg.read("notifications.ini")

# Notifications for monthly achievement notifications
ACHIEVE_LEV1 = cfg['Monthly Achievement']['Below_Minimum']
ACHIEVE_LEV2 = cfg['Monthly Achievement']['Below_Optimal']
ACHIEVE_LEV3 = cfg['Monthly Achievement']['Above_Optimal']

# Notifications for daily score notifications
SCORE_DAY_LEV1 = cfg['Score Based']['Below_Minimum']
SCORE_DAY_LEV2 = cfg['Score Based']['Below_Optimal']
SCORE_DAY_LEV3 = cfg['Score Based']['Above_Optimal']

# Notifications for weekly score notifications
# Auto generated
SCORE_WEEK_LEV1 = SCORE_DAY_LEV1.replace("yesterday", "last week")
SCORE_WEEK_LEV2 = SCORE_DAY_LEV2.replace("yesterday", "last week")
SCORE_WEEK_LEV3 = SCORE_DAY_LEV3.replace("yesterday", "last week")

# Notifications for monthly score notifications
# Auto generated
SCORE_MONTH_LEV1 = SCORE_DAY_LEV1.replace("yesterday", "last month")
SCORE_MONTH_LEV2 = SCORE_DAY_LEV2.replace("yesterday", "last month")
SCORE_MONTH_LEV3 = SCORE_DAY_LEV3.replace("yesterday", "last month")