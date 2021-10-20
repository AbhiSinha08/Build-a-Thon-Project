"""File: bots/mail.py"""
""" To connect to SMTP server and send mails """

# getting email id details from config file
from cfg import MAIL_ID, MAIL_PASSWORD, SMTP_SERVER, SMTP_PORT
import smtplib # Library to send mails

try:
    # Connecting to SMTP Server
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
except:
    print("Please Check your internet connection for sending mails and messages!")
    exit()
server.starttls()

try:
    # Logging in with details in config file
    server.login(MAIL_ID, MAIL_PASSWORD)
except smtplib.SMTPAuthenticationError:
    print("Unable to sign in!")
    print("Please Check email id and pssword in config.ini")
    exit()

# After verifying login details
server.quit()

# Function to actually send mails to given email
def sendMail(reciever, sub, body):
    try:
        # Connecting to 
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(MAIL_ID, MAIL_PASSWORD)
    except:
        print("Please Check your internet connection for sending mails and messages!")

    # Composing Message
    message = f'Subject: {sub}\n\n{body}'

    # Sending Mail
    server.sendmail(MAIL_ID, reciever, message)
    print("mail sent to ", reciever)

    # Quiting Server
    server.quit()

if __name__ == '__main__':
    pass