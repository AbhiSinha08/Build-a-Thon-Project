from cfg import MAIL_ID, MAIL_PASSWORD
import smtplib

try:
    server = smtplib.SMTP("smtp.gmail.com" , 587)
except:
    print("Please Check your internet connection for sending mails and messages!")
    exit()
server.starttls()

try:    
    server.login(MAIL_ID,MAIL_PASSWORD)
except smtplib.SMTPAuthenticationError:
    print("Unable to sign in!")
    print("Please Check email id and pssword in config.ini")
    exit()


def sendMail(reciever, sub, body):
    message = 'Subject: {}\n\n{}'.format(sub,body)
    server.sendmail(MAIL_ID,reciever,message)

if __name__ == '__main__':
    pass