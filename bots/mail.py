from cfg import MAIL_ID, MAIL_PASSWORD, SMTP_SERVER, SMTP_PORT
import smtplib

try:
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
except:
    print("Please Check your internet connection for sending mails and messages!")
    exit()
server.starttls()

try:    
    server.login(MAIL_ID, MAIL_PASSWORD)
except smtplib.SMTPAuthenticationError:
    print("Unable to sign in!")
    print("Please Check email id and pssword in config.ini")
    exit()
    
server.quit()


def sendMail(reciever, sub, body):
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    except:
        print("Please Check your internet connection for sending mails and messages!")
    server.starttls()
    try:    
        server.login(MAIL_ID, MAIL_PASSWORD)
    except smtplib.SMTPAuthenticationError:
        print("Unable to sign in!")
        print("Please Check email id and pssword in config.ini")

    message = f'Subject: {sub}\n\n{body}'
    server.sendmail(MAIL_ID, reciever, message)
    print("mail sent to ", reciever)
    server.quit()

if __name__ == '__main__':
    pass