import configparser

cfg = configparser.ConfigParser()
cfg.read("config.ini")

HOST = cfg['mysql']['host']
PORT = int(cfg['mysql']['port'])
USER = cfg['mysql']['user']
PASSWORD = cfg['mysql']['password']
DATABASE = cfg['mysql']['db']

ADMIN_PW = cfg['admin portal']['password']

MAIL_ID = cfg['mail bot']['mail_id']
MAIL_PASSWORD = cfg['mail bot']['password']
SMTP_SERVER = cfg['mail bot']['smtp_server']
SMTP_PORT = int(cfg['mail bot']['port'])
SUBJECT = cfg['mail bot']['subject']

WA_OPTION = cfg['whatsapp']['enable'].upper()
if WA_OPTION == "YES" or WA_OPTION == "Y":
    WA_OPTION = True
else:
    WA_OPTION = False

API = cfg['sms bot']['API']


cfg.read("notifications.ini")

ACHIEVE_LEV1 = cfg['Monthly Achievement']['Below_Minimum']
ACHIEVE_LEV2 = cfg['Monthly Achievement']['Below_Optimal']
ACHIEVE_LEV3 = cfg['Monthly Achievement']['Above_Optimal']

SCORE_DAY_LEV1 = cfg['Score Based']['Below_Minimum']
SCORE_DAY_LEV2 = cfg['Score Based']['Below_Optimal']
SCORE_DAY_LEV3 = cfg['Score Based']['Above_Optimal']

SCORE_WEEK_LEV1 = SCORE_DAY_LEV1.replace("yesterday", "last week")
SCORE_WEEK_LEV2 = SCORE_DAY_LEV2.replace("yesterday", "last week")
SCORE_WEEK_LEV3 = SCORE_DAY_LEV3.replace("yesterday", "last week")

SCORE_MONTH_LEV1 = SCORE_DAY_LEV1.replace("yesterday", "last month")
SCORE_MONTH_LEV2 = SCORE_DAY_LEV2.replace("yesterday", "last month")
SCORE_MONTH_LEV3 = SCORE_DAY_LEV3.replace("yesterday", "last month")